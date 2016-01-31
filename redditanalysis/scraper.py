#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import sys

import praw
from requests.exceptions import HTTPError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

from . import COMMENT_ATTRS
from settings import Config
from .models import Submission, Comment


logging.basicConfig(level="WARN")
logger = logging.getLogger(__name__)

# project configuration settings
cfg = Config()
if not cfg.USERNAME:
    logger.error("Username in settings must be set. Exiting...")
    sys.exit()

# setup DB session
engine = create_engine(cfg.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()


def _model_columns(db_model):
    """Return the columns names from a given DB model.
    """
    return [c.name for c in db_model.__table__.columns]


def process_redditor(redditor, limit, count_word_freqs, max_threshold):
    """Parse submissions and comments for the given Redditor.

    :param limit: the maximum number of submissions to scrape from the
        subreddit

    :param count_word_freqs: if False, only count a word once per text block
        (title, selftext, comment body) rather than incrementing the total for
        for each instance.

    :param max_threshold: maximum relative frequency in the text a word can
        appear to be considered in word counts. prevents word spamming in a
        single submission.

    """
    entries = redditor.get_overview(limit=limit)
    for entry in tqdm(iterable=entries, nested=True):
        if isinstance(entry, praw.objects.Comment):
            # parse comment
            parse_text(
                text=entry.body,
                count_word_freqs=count_word_freqs,
                max_threshold=max_threshold
                )
        else:
            # parse submission
            parse_submission(
                submission=entry,
                count_word_freqs=count_word_freqs,
                max_threshold=max_threshold,
                include_comments=False
                )


def process_comments(comments):
    """Inject comments data into the database.
    """
    for c in tqdm(comments, desc="Injecting comments into DB"):
        Comment.create(session, **c)


def parse_comments(submission):
    """Parse a submission's comments according to the structure of the
    database model schema.

    :param submission_id: the source submission's id

    :return: a list of Submission comment dicts.
    """
    comments = []
    submission.replace_more_comments()
    for c in praw.helpers.flatten_tree(submission.comments):
        comment_dict = c.__dict__

        # NOTE: author is a special case (and must be present)
        author = c.author.name if hasattr(c.author, "name") else None
        if not author:
            continue

        comment = {
            "submission_id": submission.id,
            "author": author
        }
        del comment_dict["author"]  # no longer needed
        for k in _model_columns(Comment):
            if k in comment_dict:
                comment[k] = comment_dict[k]
        comments.append(comment)

    return comments


def process_submission(submission):
    """Injecting submission data into the database.
    """
    logger.info(process_submission.__doc__)
    Submission.create(session, **submission)


def parse_submission(submission, include_comments=True):
    """Parse a submission's text and body (if applicable) according to the
    structure of the database model schema.

    :param include_comments: include the submission's comments when True

    :return: Submission info and comments (if applicable).
    """
    sub_dict = submission.__dict__
    info = {
        "fullname": submission.fullname  # only available as attribute
    }
    # treat author as special case to avoid additional API requests
    info["author"] = sub_dict["author"].name if sub_dict["author"] else ""
    del sub_dict["author"]

    # collect data, given the columns in the db model
    for k in _model_columns(Submission):
        if k in sub_dict:
            info[k] = sub_dict[k]

    # parse all the comments for the submission
    comments = None
    if include_comments:
        comments = parse_comments(submission)

    return info, comments


def process_subreddit(subreddit, period, limit, cached_ids=None):
    """Parse comments, title text, and selftext in a given subreddit.

    :param period: the time period to scrape the subreddit over (day, week,
    month, etc.)

    :param limit: the maximum number of submissions to scrape from the
    subreddit
    """
    # set submission query params
    params = {
        "t": period,
        "show": "all"
    }

    # process submissions
    submissions = subreddit.get_new(limit=limit, params=params)
    for s in tqdm(submissions, desc="Submissions", nested=True):
        if cached_ids is not None and s.id not in cached_ids:
            try:
                submission, comments = parse_submission(s)
                process_comments(comments)
                process_submission(submission)
            except HTTPError as exc:
                logger.error(
                    "Skipping submission {0} due to HTTP status {1} error. "
                    "Continuing...".format(
                        submission.permalink.encode("UTF-8"),
                        exc.response.status_code)
                        )
            except ValueError:  # Occurs occasionally with empty responses
                logger.error(
                    "Skipping submission {0} due to ValueError.".format(
                        submission.permalink.encode("UTF-8")))


def main():
    # setup PRAW handler
    handler = None
    if cfg.MULTIPROCESS:
        handler = praw.handlers.MultiprocessHandler()

    # open connection to Reddit
    user_agent = "Reddit analytics scraper by /u/{}".format(cfg.USERNAME)

    r = praw.Reddit(user_agent=user_agent, handler=handler)
    r.config.decode_html_entities = True

    # get a list of cached submission IDs
    cached_submissions = session.query(Submission).all()
    cached_ids = [s.id for s in cached_submissions]

    # process targets
    for target in tqdm(iterable=cfg.TARGETS, desc="Reddit targets"):
        if target.startswith("/r/"):
            subreddit = target[3:]
            process_subreddit(
                subreddit=r.get_subreddit(subreddit),
                period=cfg.PERIOD,
                limit=cfg.LIMIT,
                cached_ids=cached_ids
                )
        elif target.startswith("/u/"):
            redditor = target[3:]
            process_redditor(
                redditor=r.get_redditor(redditor),
                limit=cfg.LIMIT
                )
        else:
            logger.error(
                "\"{}\" is an invalid target. Skipping...".format(target))


if __name__ == '__main__':
    main()

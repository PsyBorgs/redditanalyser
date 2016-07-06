#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

import praw
from requests.exceptions import HTTPError
from tqdm import tqdm

from . import cfg, COMMENT_ATTRS, logger, reddit, session
from .models import Submission, Comment


def _model_columns(db_model):
    """Return the columns names from a given DB model.
    """
    return [c.name for c in db_model.__table__.columns]


def process_comments(session, comments):
    """Inject comments data into the database.
    """
    for c in tqdm(comments, desc="Injecting comments into DB"):
        Comment.create(session, **c)


def process_submission(session, submission):
    """Inject submission data into the database.
    """
    logger.debug(process_submission.__doc__)
    Submission.create(session, **submission)


def process_redditor(session, redditor, limit):
    """Process submissions and comments for the given Redditor.

    :param limit: the maximum number of submissions to scrape from the
        subreddit
    """
    entries = redditor.get_overview(limit=limit)
    for entry in tqdm(iterable=entries, nested=True):
        if isinstance(entry, praw.objects.Comment):
            # process comment
            process_comments(session, [entry])
        else:
            # process submission
            process_submission(session, entry)


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


def process_subreddit(session, subreddit, period, limit, cached_ids=None):
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
                process_comments(session, comments)
                process_submission(session, submission)
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
    # get a list of cached submission IDs
    cached_submissions = session.query(Submission).all()
    cached_ids = [s.id for s in cached_submissions]

    # process targets
    for target in tqdm(iterable=cfg.TARGETS, desc="Reddit targets"):
        if target.startswith("/r/"):
            subreddit = target[3:]
            process_subreddit(
                session=session,
                subreddit=reddit.get_subreddit(subreddit),
                period=cfg.PERIOD,
                limit=cfg.LIMIT,
                cached_ids=cached_ids
                )
        elif target.startswith("/u/"):
            redditor = target[3:]
            process_redditor(
                session=session,
                redditor=reddit.get_redditor(redditor),
                limit=cfg.LIMIT
                )
        else:
            logger.error(
                "\"{}\" is an invalid target. Skipping...".format(target))


if __name__ == '__main__':
    main()

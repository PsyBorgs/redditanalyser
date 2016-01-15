#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging

import pandas as pd
import praw
import tqdm
from bs4 import BeautifulSoup
from markdown import markdown
from requests.exceptions import HTTPError

from . import DATA_DIR, COMMENT_ATTRS
from settings import Settings


logger = logging.getLogger(__name__)


def cache_submission_comments(submission):
    logger.debug("Caching comments...")
    submission_df = pd.DataFrame(submission, columns=COMMENT_ATTRS)
    csv_path = os.path.join(
        DATA_DIR, 'comments', '{}.csv'.format(submission.fullname))
    comments_df.to_csv(csv_path, encoding='utf-8')


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
            process_submission(
                submission=entry,
                count_word_freqs=count_word_freqs,
                max_threshold=max_threshold,
                include_comments=False
                )


def process_submission(submission, count_word_freqs, max_threshold, include_comments=True):
    """Parse a submission's text and body (if applicable).

    :param count_word_freqs: if False, only count a word once per text block
        (title, selftext, comment body) rather than incrementing the total for
        for each instance.

    :param max_threshold: maximum relative frequency in the text a word can
        appear to be considered in word counts. prevents word spamming in a
        single submission.

    :param include_comments: include the submission's comments when True

    """
    # parse the title of the submission
    parse_text(
        text=submission.title,
        count_word_freqs=count_word_freqs,
        max_threshold=max_threshold,
        is_markdown=False
        )

    # parse all the comments for the submission
    if include_comments:
        submission.replace_more_comments()
        for comment in praw.helpers.flatten_tree(submission.comments):
            parse_text(
                text=comment.body,
                count_word_freqs=count_word_freqs,
                max_threshold=max_threshold
                )

    # parse the selftext of the submission (if applicable)
    if submission.is_self:
        parse_text(
            text=submission.selftext,
            count_word_freqs=count_word_freqs,
            max_threshold=max_threshold
            )


def process_subreddit(subreddit, period, limit, count_word_freqs, max_threshold):
    """Parse comments, title text, and selftext in a given subreddit.

    :param period: the time period to scrape the subreddit over (day, week,
    month, etc.)

    :param limit: the maximum number of submissions to scrape from the
    subreddit

    :param count_word_freqs: if False, only count a word once per text block
        (title, selftext, comment body) rather than incrementing the total for
        for each instance.

    :param max_threshold: maximum relative frequency in the text a word can
        appear to be considered in word counts. prevents word spamming in a
        single submission.

    """

    # set submission query params
    params = {
        "t": period,
        "show": "all"
    }

    # process submissions
    submissions = subreddit.get_new(limit=limit, params=params)
    for submission in tqdm(
            iterable=submissions, desc="Submissions", nested=True):
        try:
            process_submission(submission=submission,
                               count_word_freqs=count_word_freqs,
                               max_threshold=max_threshold)
        except HTTPError as exc:
            logger.error("Skipping submission {0} due to HTTP status {1}"
                             " error. Continuing..."
                             .format(submission.permalink.encode("UTF-8"),
                                     exc.response.status_code))
        except ValueError:  # Occurs occasionally with empty responses
            logger.error("Skipping submission {0} due to ValueError."
                             .format(submission.permalink.encode("UTF-8")))



def main():
    logging.basicConfig(level="WARN")

    # get settings
    settings = Settings()

    # open connection to Reddit
    handler = None
    if options.multiprocess:
        handler = praw.handlers.MultiprocessHandler()
    user_agent = "Reddit scraper bot by /u/{}".format(settings.username)

    reddit = praw.Reddit(user_agent=user_agent, handler=handler)
    reddit.config.decode_html_entities = True

    # process targets
    for target in tqdm(iterable=targets, desc="Reddit targets"):
        if target.startswith("/r/"):
            process_subreddit(
                subreddit=reddit.get_subreddit(target),
                period=settings.period,
                limit=settings.limit,
                count_word_freqs=settings.count_word_freqs,
                max_threshold=settings.max_threshold
                )
        elif target.startswith("/u/"):
            process_redditor(
                redditor=reddit.get_redditor(target),
                limit=settings.limit,
                count_word_freqs=settings.count_word_freqs,
                max_threshold=settings.max_threshold
                )
        else:
            logger.error("\"{}\" is an invalid target. Skipping."
                .format(target))


if __name__ == '__main__':
    main()

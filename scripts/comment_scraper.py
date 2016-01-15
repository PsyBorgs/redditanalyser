#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging

import praw
import pandas as pd
import tqdm

from . import DATA_DIR
from settings import Settings


logger = logging.getLogger(__name__)


# note: including `author` slows comment requests considerably
COMMENT_ATTRS = [
    'id',
    'created_utc',
    # 'author',
    'body',
    'score',
    'ups',
    'downs',
    'subreddit',
    'subreddit_id',
    'controversiality',
    'is_root',
    'parent_id',
    'gilded',
    'permalink',
]
USER_AGENT = "Comment thread scraper by /u/PsyBorgs"


def cache_submission(r, submission_id):
    logger.debug("Downloading submission comments...")
    submission = r.get_submission(submission_id=submission_id)
    submission.replace_more_comments()

    logger.debug("Flattening and filtering comments...")
    comments = []
    for c in praw.helpers.flatten_tree(submission.comments):
        if isinstance(c, praw.objects.Comment):
            comment = {}
            for attr in COMMENT_ATTRS:
                comment[attr] = getattr(c, attr)
            comments.append(comment)

    logger.debug("Caching comments...")
    comments_df = pd.DataFrame(comments, columns=COMMENT_ATTRS)
    csv_path = os.path.join(
        DATA_DIR, 'comments', '{}.csv'.format(submission_id))
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
    for entry in with_status(iterable=redditor.get_overview(limit=limit)):
        if isinstance(entry, praw.objects.Comment):  # Parse comment
            parse_text(text=entry.body, count_word_freqs=count_word_freqs,
                       max_threshold=max_threshold)
        else:  # Parse submission
            process_submission(submission=entry,
                               count_word_freqs=count_word_freqs,
                               max_threshold=max_threshold,
                               include_comments=False)


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
    if include_comments:  # parse all the comments for the submission
        submission.replace_more_comments()
        for comment in praw.helpers.flatten_tree(submission.comments):
            parse_text(text=comment.body, count_word_freqs=count_word_freqs,
                       max_threshold=max_threshold)

    # parse the title of the submission
    parse_text(text=submission.title, count_word_freqs=count_word_freqs,
               max_threshold=max_threshold, is_markdown=False)

    # parse the selftext of the submission (if applicable)
    if submission.is_self:
        parse_text(text=submission.selftext, count_word_freqs=count_word_freqs,
                   max_threshold=max_threshold)


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

    # determine period to count the words over
    params = {"t": period}
    for submission in with_status(iterable=subreddit.get_top(limit=limit, params=params)):
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

    # connect to Reddit
    r = praw.Reddit(user_agent=settings.username)

    for target in targets:
        if target.startswith("/r/"):
            is_subreddit = True
        elif target.startswith("/u/"):
            is_subreddit = False
        else:
            logger.error("\"{}\" is an invalid target. Skipping."
                .format(target))
    submission_id = "dtg4j"
    cache_submission(r, submission_id)


if __name__ == '__main__':
    main()

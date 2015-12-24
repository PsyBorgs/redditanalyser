#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging

import praw
import pandas as pd

from . import DATA_DIR


logger = logging.getLogger(__name__)


COMMENT_ATTRS = [
    'id',
    'created_utc',
    'author',
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
    csv_path = os.path.join(DATA_DIR, 'comments', '{}.csv'.format(submission_id))
    comments_df.to_csv(csv_path, encoding='utf-8')


def main():
    logging.basicConfig(level="DEBUG")

    # connect to Reddit
    r = praw.Reddit(user_agent=USER_AGENT)

    submission_id = "dtg4j"
    cache_submission(r, submission_id)


if __name__ == '__main__':
    main()

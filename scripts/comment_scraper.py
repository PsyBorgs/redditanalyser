#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import praw
import pandas as pd

from . import DATA_DIR

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
SUBMISSION_ID = "1p1j6c"

# connect to Reddit
user_agent = "Comment thread scraper by /u/PsyBorgs"
r = praw.Reddit(user_agent=user_agent)

# get comment thread and populate dict
submission = r.get_submission(submission_id=SUBMISSION_ID)
submission.replace_more_comments()

flat_comments = praw.helpers.flatten_tree(submission.comments)
comments = []
for c in flat_comments:
    if isinstance(c, praw.objects.Comment):
        comment = {}
        for attr in COMMENT_ATTRS:
            comment[attr] = getattr(c, attr)
        comments.append(comment)

# save comments
comments_df = pd.DataFrame(comments, columns=COMMENT_ATTRS)
csv_path = os.path.join(DATA_DIR, 'comments-{}.csv'.format(SUBMISSION_ID))
comments_df.to_csv(csv_path, encoding='utf-8')

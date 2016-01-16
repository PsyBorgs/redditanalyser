# -*- coding: utf-8 -*-

# Attributes of interest for comment objects
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

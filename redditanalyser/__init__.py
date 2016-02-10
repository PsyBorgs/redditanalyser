# -*- coding: utf-8 -*-
import logging

from settings import Config


logging.basicConfig(level="WARN")
logger = logging.getLogger(__name__)

# Project configuration settings
cfg = Config()
if not cfg.USERNAME:
    logger.error("Username in settings must be set. Exiting...")
    sys.exit()

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

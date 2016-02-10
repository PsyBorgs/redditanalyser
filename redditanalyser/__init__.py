# -*- coding: utf-8 -*-
import logging

import praw

from settings import Config
from .database import create_db_session


logging.basicConfig(level="WARN")
logger = logging.getLogger(__name__)

# Project configuration settings
cfg = Config()
if not cfg.USERNAME:
    logger.error("Username in settings must be set. Exiting...")
    sys.exit()

# setup DB session
session = create_db_session(cfg.SQLALCHEMY_DATABASE_URI)

# setup PRAW handler
handler = None
if cfg.MULTIPROCESS:
    handler = praw.handlers.MultiprocessHandler()

# setup and open connection to Reddit
user_agent = "Reddit analytics scraper by /u/{}".format(cfg.USERNAME)

reddit = praw.Reddit(user_agent=user_agent, handler=handler)
reddit.config.decode_html_entities = True

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

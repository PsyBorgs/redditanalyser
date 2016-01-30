# -*- coding: utf-8 -*-
import os


class Config(object):
    """Settings for your Reddit scraper project.

    Note: Every object must have a value.
    """
    # Project paths
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))  # This directory
    APP_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, 'redditanalysis'))
    DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

    # Your Reddit username for the bot.
    # IMPORTANT: This must be set before running the code.
    USERNAME = None

    # A list of subreddits that you are targeting for scraping.
    # Note: enter `/r/TARGET` for subreddits or `/u/TARGET` for users
    TARGETS = [
        "/r/science",
        "/r/technology"
    ]

    # Period to count words over; e.g., day/week/month/year/all
    PERIOD = "all"

    # Maximum number of submissions/comments to return
    # Note: For no limit, set value to None
    LIMIT = None

    # Maximum relative frequency in the text a word can appear to be considered
    # in word counts (prevents word spamming in a single submission)
    MAX_THRESHOLD = 0.34

    # Count repeated words in text blocks (titles, selftexts, comment bodies)
    # and increment the word count, rather than counting each word occurrence
    # only once per block
    COUNT_WORD_FREQS = True

    # Enable PRAW multiprocess support
    MULTIPROCESS = True

    # Set database type (the default settings should suffice)
    DB_PATH = os.path.join(PROJECT_ROOT, 'reddit.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)

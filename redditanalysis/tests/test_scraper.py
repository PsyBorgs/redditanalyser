import pytest
import praw

from settings import Config
from redditanalysis import scraper
from redditanalysis.models import Submission


cfg = Config()
# setup PRAW
user_agent = "Reddit analytics scraper by /u/{}".format(cfg.USERNAME)
reddit = praw.Reddit(user_agent=user_agent)


def test_parse_submission():
    submission_id = "42y3i7"
    submission = reddit.get_submission(submission_id=submission_id)
    s, comments = scraper.parse_submission(submission, Submission)

    model_columns = [c.name for c in Submission.__table__.columns]
    assert sorted(s.keys()) == sorted(model_columns)

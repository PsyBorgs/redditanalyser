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

    # matchup with DB model schema
    model_columns = [c.name for c in Submission.__table__.columns]
    assert sorted(s.keys()) == sorted(model_columns)

    # individual values
    expected_values = [
        ('fullname', "t3_{}".format(submission_id)),
        ('created_utc', 1453910407.0),
        ('subreddit_id', 't5_mouw'),
        ('permalink', 'https://www.reddit.com/r/science/comments/42y3i7'
                      '/static_stretching_before_exercise_proven_to_be/'),
        ('author', 'Fang88'),
        ('title', 'Static stretching before exercise proven to be beneficial'
                  ' in new metastudy.'),
        ('selftext', ''),
        ('ups', 5),
        ('downs', 0),
        ('score', 5),
        ('num_comments', 0)
    ]
    for k, v in expected_values:
        assert s[k] == v

import pytest
import praw

from settings import Config
from redditanalysis import scraper
from redditanalysis.models import Submission, Comment


cfg = Config()
# setup PRAW
user_agent = "Reddit analytics scraper by /u/{}".format(cfg.USERNAME)
reddit = praw.Reddit(user_agent=user_agent)


def test_parse_submission_42y3i7():
    submission_id = "42y3i7"
    submission = reddit.get_submission(submission_id=submission_id)

    # si = submission info; sc = submission comments
    si, sc = scraper.parse_submission(submission, Submission)

    # matchup with DB model schema
    assert sorted(si.keys()) == sorted(scraper._model_columns(Submission))

    # individual values
    expected_values = [
        ('id', submission_id),
        ('fullname', "t3_{}".format(submission_id)),
        ('created_utc', 1453910407.0),
        ('subreddit_id', 't5_mouw'),
        ('permalink', 'https://www.reddit.com/r/science/comments/42y3i7'
                      '/static_stretching_before_exercise_proven_to_be/'),
        ('author', 'Fang88'),
        ('title', 'Static stretching before exercise proven to be beneficial'
                  ' in new metastudy.'),
        ('selftext', ''),
        ('num_comments', 0)
    ]
    for k, v in expected_values:
        assert si[k] == v

    # scores
    expected_scores = [
        ('ups', 4),
        ('downs', 0),
        ('score', 4)
    ]
    for k, v in expected_scores:
        assert si[k] >= v

    # comments
    assert not sc


def _comments_for_2zxglv(sc, submission_id):
    """Shared set of assertions for submission 2zxglv.
    """
    assert isinstance(sc, list)
    assert len(sc) == 7

    # matchup first comment keys with DB model schema
    assert sorted(sc[0].keys()) == sorted(scraper._model_columns(Comment))

    # first comment individual values
    c0_expected_values = [
        ('id', "cpnchwj"),
        ('created_utc', 1427062942.0),
        ('submission_id', submission_id),
        ('name', "t1_cpnchwj"),
        ('parent_id', "t3_2zxglv"),
        ('author', "hansolo669"),
    ]
    for k, v in c0_expected_values:
        assert sc[0][k] == v

    assert sc[0]["body"].startswith("You could always try paginating")

    # scores
    c0_expected_scores = [
        ('ups', 1),
        ('downs', 0),
        ('score', 1)
    ]
    for k, v in c0_expected_scores:
        assert sc[0][k] >= v


def test_parse_submission_2zxglv():
    submission_id = "2zxglv"
    submission = reddit.get_submission(submission_id=submission_id)

    # si = submission info; sc = comments
    si, sc = scraper.parse_submission(submission, Submission)

    # selftext
    assert si["selftext"].startswith(
        "E.g. Download all comments in a subreddit from the last 2 months.")

    # individual values
    expected_values = [
        ('id', submission_id),
        ('fullname', "t3_{}".format(submission_id)),
        ('created_utc', 1427051022.0),
        ('subreddit_id', 't5_2qizd'),
        ('permalink', 'https://www.reddit.com/r/redditdev/comments/2zxglv/'
                      'best_way_to_download_comments_from_a_subreddit/'),
        ('author', 'teh_shit'),
        ('title', 'Best way to download comments from a subreddit, given a '
                  'time interval?'),
        ('num_comments', 7)
    ]
    for k, v in expected_values:
        assert si[k] == v

    # scores
    expected_scores = [
        ('ups', 4),
        ('downs', 0),
        ('score', 4)
    ]
    for k, v in expected_scores:
        assert si[k] >= v

    # comments
    _comments_for_2zxglv(sc, submission_id=submission_id)


def test_parse_comments_2zxglv():
    submission_id = "2zxglv"
    submission = reddit.get_submission(submission_id=submission_id)
    sc = scraper.parse_comments(submission)

    _comments_for_2zxglv(sc, submission_id=submission_id)

import pytest

from app.models import Submission, Comment


MOCK_SUBMISSION = {
    'permalink': (u'https://www.reddit.com/r/fake/comments'
                  u'/000000/submission_title/'
                  ),
    'score': 100,
    'author': u'fakeuser1',
    'num_comments': 500,
    'downs': 0,
    'title': u'Submission title',
    'created_utc': 1415713246.0,
    'subreddit_id': u't5_000000',
    'ups': 100,
    'selftext': u'',
    'fullname': u't3_aaaaaa',
    'archived': True,
    'id': u'aaaaaa'
}


def test_submission_model(session):
    Submission.create(session, **MOCK_SUBMISSION)

    db_submissions = session.query(Submission).all()

    assert len(db_submissions) == 1

    db_s = db_submissions[0]
    for k in MOCK_SUBMISSION.keys():
        assert getattr(db_s, k) == MOCK_SUBMISSION[k]

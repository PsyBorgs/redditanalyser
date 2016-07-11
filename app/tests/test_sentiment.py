import pytest
from sqlalchemy.orm import joinedload

from app.tests import const
from app.models import (
    Submission, Comment, SubmissionSentiment, CommentSentiment)
from app import sentiment


def test_comment_sentiment(session):
    s = Submission.create(session, **const.MOCK_SUBMISSION)

    c = Comment.create(session, **const.MOCK_COMMENT1)
    cs = sentiment.comment_sentiment(c)

    expected_keys = ['comment_id', 'polarity', 'subjectivity']
    assert sorted(cs.keys()) == sorted(expected_keys)

    assert isinstance(cs['polarity'], float)
    assert isinstance(cs['subjectivity'], float)


def test_comment_sentiment_avg(session):
    s = Submission.create(session, **const.MOCK_SUBMISSION)

    c1 = Comment.create(session, **const.MOCK_COMMENT1)
    c1_sentiment = sentiment.comment_sentiment(c1)
    c1s = CommentSentiment.create(session, **c1_sentiment)

    c2 = Comment.create(session, **const.MOCK_COMMENT2)
    c2_sentiment = sentiment.comment_sentiment(c2)
    c2s = CommentSentiment.create(session, **c2_sentiment)

    comments = session.query(Comment).\
        options(joinedload('sentiment')).\
        all()
    csa = sentiment.comment_sentiment_avg(comments)
    csa.update({'submission_id': s.id})

    expected_keys = ['submission_id', 'polarity', 'subjectivity']
    assert sorted(csa.keys()) == sorted(expected_keys)

    assert isinstance(csa['polarity'], float)
    assert isinstance(csa['subjectivity'], float)

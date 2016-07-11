import pytest
from textblob import TextBlob

from app.models import Submission, Comment, CommentSentiment
from app.tests.const import MOCK_SUBMISSION, MOCK_COMMENT1, MOCK_COMMENT2


def test_submission_model(session):
    s = Submission.create(session, **MOCK_SUBMISSION)

    db_submissions = session.query(Submission).all()

    assert len(db_submissions) == 1

    db_s = db_submissions[0]
    for k in MOCK_SUBMISSION.keys():
        assert getattr(db_s, k) == MOCK_SUBMISSION[k]


def test_comment_model(session):
    s = Submission.create(session, **MOCK_SUBMISSION)
    c1 = Comment.create(session, **MOCK_COMMENT1)
    c2 = Comment.create(session, **MOCK_COMMENT2)

    db_submissions = session.query(Submission).all()
    db_comments = session.query(Comment).all()

    assert db_submissions[0].comments[0] == c1
    assert db_submissions[0].comments[1] == c2
    assert len(db_comments) == 2

    db_c1 = db_comments[0]
    for k in MOCK_COMMENT1.keys():
        assert getattr(db_c1, k) == MOCK_COMMENT1[k]

    # test relationship
    assert s.comments == db_comments


def test_commentsentiment_model(session):
    s = Submission.create(session, **MOCK_SUBMISSION)

    c1 = Comment.create(session, **MOCK_COMMENT1)
    c1_blob = TextBlob(c1.body)
    c1_sentiment = {
        'comment_id': c1.id,
        'polarity': c1_blob.sentiment.polarity,
        'subjectivity': c1_blob.sentiment.subjectivity
    }
    c1s = CommentSentiment.create(session, **c1_sentiment)

    c2 = Comment.create(session, **MOCK_COMMENT2)
    c2_blob = TextBlob(c2.body)
    c2_sentiment = {
        'comment_id': c2.id,
        'polarity': c2_blob.sentiment.polarity,
        'subjectivity': c2_blob.sentiment.subjectivity
    }
    c2s = CommentSentiment.create(session, **c2_sentiment)

    assert c1s.id == 1
    assert c2s.id == 2
    for k in c1_sentiment.keys():
        assert getattr(c1s, k) == c1_sentiment[k]

    # test relationship
    assert c1.sentiment == c1s

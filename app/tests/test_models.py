import pytest
from textblob import TextBlob

from app.models import Submission, Comment, CommentSentiment
from app.tests.const import MOCK_SUBMISSION, MOCK_COMMENT


def test_submission_model(session):
    s = Submission.create(session, **MOCK_SUBMISSION)

    db_submissions = session.query(Submission).all()

    assert len(db_submissions) == 1

    db_s = db_submissions[0]
    for k in MOCK_SUBMISSION.keys():
        assert getattr(db_s, k) == MOCK_SUBMISSION[k]


def test_comment_model(session):
    s = Submission.create(session, **MOCK_SUBMISSION)
    c = Comment.create(session, **MOCK_COMMENT)

    db_submissions = session.query(Submission).all()
    db_comments = session.query(Comment).all()

    assert db_submissions[0].comments[0] == c
    assert len(db_comments) == 1

    db_c = db_comments[0]
    for k in MOCK_COMMENT.keys():
        assert getattr(db_c, k) == MOCK_COMMENT[k]

    # test relationship
    assert s.comments == db_comments


def test_commentsentiment_model(session):
    s = Submission.create(session, **MOCK_SUBMISSION)
    c = Comment.create(session, **MOCK_COMMENT)

    comment_blob = TextBlob(c.body)
    comment_sentiment = {
        'comment_id': c.id,
        'polarity': comment_blob.sentiment.polarity,
        'subjectivity': comment_blob.sentiment.subjectivity
    }

    cs = CommentSentiment.create(session, **comment_sentiment)

    assert cs.id == 1
    for k in comment_sentiment.keys():
        assert getattr(cs, k) == comment_sentiment[k]

    # test relationship
    assert c.sentiment == cs

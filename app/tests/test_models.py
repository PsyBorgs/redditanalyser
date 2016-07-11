import pytest
from textblob import TextBlob
from sqlalchemy.orm import joinedload

from app.models import (
    Submission, Comment, CommentSentiment, SubmissionSentiment)
from app.sentiment import comment_sentiment_avg
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


def _comment_sentiment(comment):
    comment_blob = TextBlob(comment.body)
    return {
        'comment_id': comment.id,
        'polarity': comment_blob.sentiment.polarity,
        'subjectivity': comment_blob.sentiment.subjectivity
    }


def test_commentsentiment_model(session):
    s = Submission.create(session, **MOCK_SUBMISSION)

    c1 = Comment.create(session, **MOCK_COMMENT1)
    c1_sentiment = _comment_sentiment(c1)
    c1s = CommentSentiment.create(session, **c1_sentiment)

    c2 = Comment.create(session, **MOCK_COMMENT2)
    c2_sentiment = _comment_sentiment(c2)
    c2s = CommentSentiment.create(session, **c2_sentiment)

    # test object form
    for k in c1_sentiment.keys():
        assert getattr(c1s, k) == c1_sentiment[k]

    # test relationship
    assert c1.sentiment == c1s

    # test values
    assert c1s.id == 1
    assert c1s.polarity > 0.5
    assert c1s.subjectivity > 0.8
    assert c2s.id == 2
    assert c2s.polarity < -0.5
    assert c2s.subjectivity > 0.8


def test_submissionsentiment_model(session):
    s = Submission.create(session, **MOCK_SUBMISSION)

    c1 = Comment.create(session, **MOCK_COMMENT1)
    c1_sentiment = _comment_sentiment(c1)
    c1s = CommentSentiment.create(session, **c1_sentiment)

    c2 = Comment.create(session, **MOCK_COMMENT2)
    c2_sentiment = _comment_sentiment(c2)
    c2s = CommentSentiment.create(session, **c2_sentiment)

    comments = session.query(Comment).\
        options(joinedload('sentiment')).\
        all()
    submission_sentiment = comment_sentiment_avg(comments)
    submission_sentiment.update({'submission_id': s.id})

    ss = SubmissionSentiment.create(session, **submission_sentiment)

    submission_sentiments = session.query(SubmissionSentiment).all()
    ss1 = submission_sentiments[0]

    # test object form
    assert ss1.id == 1
    assert ss1.submission_id == s.id
    for k in submission_sentiment.keys():
        assert getattr(ss1, k) == submission_sentiment[k]

    # test values
    assert ss1.polarity < 0.5 and ss1.polarity > -0.5
    assert ss1.subjectivity > 0.8

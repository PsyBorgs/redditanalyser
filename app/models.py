from .database import (
    Base,
    db,
    Column,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK
)


class Submission(Model):
    __tablename__ = 'submissions'

    id = db.Column(db.String, primary_key=True)

    created_utc = Column(db.Float, nullable=False)
    fullname = Column(db.String, nullable=False)
    subreddit_id = Column(db.String, nullable=False)
    permalink = Column(db.String, nullable=False)

    author = Column(db.String, nullable=False)
    title = Column(db.Unicode, nullable=False)
    selftext = Column(db.UnicodeText)

    ups = Column(db.Integer, nullable=False)
    downs = Column(db.Integer, nullable=False)
    score = Column(db.Integer, nullable=False)
    num_comments = Column(db.Integer, nullable=False)

    archived = Column(db.Boolean, nullable=False)

    comments = relationship('Comment', backref='submission')
    sentiment = relationship(
        'SubmissionSentiment', backref='submission', uselist=False)


class SubmissionSentiment(Model, SurrogatePK):
    __tablename__ = 'submission_sentiments'

    submission_id = ReferenceCol('submissions')

    polarity = Column(db.Float)
    subjectivity = Column(db.Float)


class Comment(Model):
    __tablename__ = 'comments'

    id = db.Column(db.String, primary_key=True)

    created_utc = Column(db.Float, nullable=False)
    parent_id = Column(db.String, nullable=False)
    name = Column(db.String, nullable=False)

    submission_id = ReferenceCol('submissions')

    author = Column(db.String)
    body = Column(db.UnicodeText, nullable=False)

    ups = Column(db.Integer, nullable=False)
    downs = Column(db.Integer, nullable=False)
    score = Column(db.Integer, nullable=False)

    sentiment = relationship(
        'CommentSentiment', backref='comment', uselist=False)


class CommentSentiment(Model, SurrogatePK):
    __tablename__ = 'comment_sentiments'

    comment_id = ReferenceCol('comments')

    polarity = Column(db.Float)
    subjectivity = Column(db.Float)

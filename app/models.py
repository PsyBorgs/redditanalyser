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


class Comment(Model):
    __tablename__ = 'comments'

    id = db.Column(db.String, primary_key=True)

    created_utc = Column(db.Float, nullable=False)
    parent_id = Column(db.String, nullable=False)
    name = Column(db.String, nullable=False)

    submission_id = ReferenceCol('submissions')
    submission = relationship('Submission', backref='comments')

    author = Column(db.String)
    body = Column(db.UnicodeText, nullable=False)

    ups = Column(db.Integer, nullable=False)
    downs = Column(db.Integer, nullable=False)
    score = Column(db.Integer, nullable=False)


class CommentSentiment(Model):
    __tablename__ = 'comment_sentiments'

    comment_id = ReferenceCol('comments')
    comment = relationship('Comment', backref='sentiment', uselist=False)

    polarity = Column(db.Float)
    subjectivity = Column(db.Float)

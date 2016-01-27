from redditanalysis.database import (
    Base,
    db,
    Column,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK
)


class Submission(Model, SurrogatePK):
    __tablename__ = 'submissions'

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

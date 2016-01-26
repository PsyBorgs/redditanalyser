from sqlalchemy import Column, Integer, String

from redditanalysis.database import (
    db,
    Column,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)


Base = declarative_base()


class Comment(Model):
    __tablename__ = 'comments'

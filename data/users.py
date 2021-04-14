import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):

    def __init__(self, name, email, hashed_password):
        self.name = name
        self.email = email
        self.hashed_password = hashed_password

    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    projects = relationship("Project", back_populates="owner")

    def has_project(self, project_name):
        return any(map(lambda x: x.name == project_name, self.projects))

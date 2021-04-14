import json
import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Project(SqlAlchemyBase):

    def __init__(self, project_name, user_created):
        self.name = project_name
        self.owner_id = user_created.id

    __tablename__ = 'projects'

    id = Column(sqlalchemy.Integer,
                primary_key=True, autoincrement=True)
    name = Column(sqlalchemy.String, nullable=True)

    owner_id = Column(sqlalchemy.Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="projects")

    designs = relationship("Design", back_populates="project")
    mockups = relationship("Mockup", back_populates="project")

    def __getitem__(self, item):
        return json.loads(self.meta)[item]

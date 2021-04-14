import json

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Design(SqlAlchemyBase):

    def __init__(self, svg, meta={}):
        self.svg = svg
        self.meta = json.dumps(meta)

    __tablename__ = 'designs'

    id = Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    project_id = Column(sqlalchemy.Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="designs")

    svg = Column(sqlalchemy.Text, nullable=True)
    meta = Column(sqlalchemy.Text, nullable=True)

    def __getitem__(self, item):
        return json.loads(self.meta)[item]

import json

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Design(SqlAlchemyBase):

    def __init__(self, svg, project, meta={}):
        self.svg = svg
        self.meta = json.dumps(meta)
        self.project_id = project.id

    __tablename__ = 'designs'

    id = Column(sqlalchemy.Integer,
                primary_key=True, autoincrement=True)

    project_id = Column(sqlalchemy.Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="designs")

    svg = Column(sqlalchemy.Text, nullable=True)
    meta = Column(sqlalchemy.Text, nullable=True)

    def __getitem__(self, item):
        return json.loads(self.meta)[item]

    def get_svg(self, include_header=True):
        if not include_header:
            return self.svg
        else:
            svg = " ".join(self.svg.split())
            svg = svg.replace(
                '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"'
                ' width="512" height="512" viewBox="0 -512 512 512">', ' ')
            return svg[:-6]

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

    def get_preview(self, s=210):
        if not self.designs:
            return """<svg width="160" height="160" viewBox="0 0 160 160" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect y="22" width="160" height="138" fill="#AAAAAA"/>
</svg>
"""
        preview = self.designs[-1].get_svg(s=s)
        return preview

    def get_design(self, design_id):
        for design in self.designs:
            if design.id == design_id:
                return design
        return None

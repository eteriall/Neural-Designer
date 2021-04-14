import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Mockup(SqlAlchemyBase, UserMixin):

    def __init__(self, link):
        self.link = link

    __tablename__ = 'mockups'

    id = Column(sqlalchemy.Integer,
                primary_key=True, autoincrement=True)

    project_id = Column(sqlalchemy.Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="mockups")

    link = Column(sqlalchemy.String, nullable=True)

    def get_images(self):
        pass

from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(), unique=True)
    name = db.Column(db.String())
    password = db.Column(db.String())

from . import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(5000), nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    url = db.Column(db.String(100), nullable=False)
    answer = db.Column(db.String(5000), nullable=True)
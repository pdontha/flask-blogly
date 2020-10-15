"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = "user_info"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    img_url = db.Column(db.String(100), default="/")
    posts = db.relationship('Post')


class Post(db.Model):
    __tablename__ = "post_table"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(15), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    user_id = db.Column(db.ForeignKey("user_info.id"))
    user = db.relationship('User')

""" SQLAlchemy models for Users """

from flask_bcrypt import Bcrypt
# from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
# db = SQLAlchemy()

from part_3 import db

class Follows(db.Model):
    """Connection of a follower <-> followed_user."""

    __tablename__ = 'follows'

    user_being_followed_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )

    user_following_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )
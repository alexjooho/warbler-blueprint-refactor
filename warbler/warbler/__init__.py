from flask import Flask
import os
from dotenv import load_dotenv

# When we imported blueprints up here, we got a circular error?

from flask import (
    Flask, render_template, request, flash, redirect, session, g, abort,
)
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

# from flask_sqlalchemy import SQLAlchemy

from .forms import CSRFProtection
# need to include "." before?
from .users.models import User

# db = SQLAlchemy()

# from forms import (
#     UserAddForm, UserEditForm, LoginForm, MessageForm, CSRFProtection,
# )
# from .users.models import (
#     db, connect_db, User, DEFAULT_IMAGE_URL, DEFAULT_HEADER_IMAGE_URL)

load_dotenv()

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
toolbar = DebugToolbarExtension(app)


# def connect_db(app):
#     """Connect this database to provided Flask app.

#     You should call this in your Flask app.
#     """

#     db.app = app
#     db.init_app(app)


# connect_db(app)


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


@app.before_request
def add_csrf_only_form():
    """Add a CSRF-only form so that every route can use it."""

    g.csrf_form = CSRFProtection()


from warbler.users.views import users_bp
from warbler.root.views import root_bp
from warbler.messages.views import messages_bp

# Register Blueprints
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(messages_bp, url_prefix='/messages')
app.register_blueprint(root_bp)


@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404


@app.after_request
def add_header(response):
    """Add non-caching headers on every request."""

    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
    response.cache_control.no_store = True
    return response

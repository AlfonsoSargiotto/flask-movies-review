from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# APP
app = Flask(__name__)

app.config["SECRET_KEY"] = environ.get("SECRET_KEY")

# ERROR HANDLERS
# from app.errors import page_not_found, internal_server_error
# app.register_error_handler(404, page_not_found)
# app.register_error_handler(500, internal_server_error)


# DB
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("SQLALCHEMY_DATABASE_URI")

# The echo flag is a shortcut to setting up SQLAlchemy logging, which is accomplished via Python’s
# standard logging module. With it enabled, we’ll see all the generated SQL produced.
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

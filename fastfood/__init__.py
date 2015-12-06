# Import flask and template operators
from flask import Flask
from flask.ext.httpauth import HTTPBasicAuth
# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS

auth = HTTPBasicAuth()

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')
app.config['DEBUG'] = True

CORS(app)

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Build the database:
# This will create the database file using SQLAlchemy
#db.create_all()

from fastfood.api import APIBase

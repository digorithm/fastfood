# Import flask and template operators
from flask import Flask
from flask_httpauth import HTTPBasicAuth
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

auth = HTTPBasicAuth()

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

CORS(app)

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Build the database:
# This will create the database file using SQLAlchemy
#db.create_all()

from fastfood.api import APIBase

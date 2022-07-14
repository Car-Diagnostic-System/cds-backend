import os

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
# Enable debug mode.
DEBUG = True
# Connect to the database
SQLALCHEMY_DATABASE_URI = 'mysql://root:password@127.0.0.1:3366/cds'
# Turn off the Flask-SQLAlchemy event system and warning
SQLALCHEMY_TRACK_MODIFICATIONS = False
JSON_SORT_KEYS = False
CORS_HEADERS = 'Content-Type'

MAX_CONTENT_LENGTH = 16 * 1024 * 1024

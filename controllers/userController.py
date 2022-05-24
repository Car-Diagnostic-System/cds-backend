from models.user import User

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
def index():
    print(User.query.all())
    print(type(User.query.all()))

    print(User.query.get(1))
    print(type(User.query.get(1)))
    return 'db'
def store():
    return db
def show(userId):
    return db
def update(userId):
    return db
def delete(userId):
    return db

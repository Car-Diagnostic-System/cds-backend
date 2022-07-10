import datetime
import jwt
from flask import request, jsonify
import bcrypt
from models.user import User
from models.role import Role
from models.car import Car

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class AuthController:
    @staticmethod
    def createAuthenticationToken():
        # NOTE: body contain email and password
        body = request.get_json()
        try:
            user = User.query.filter_by(email=body['email']).first()
            if (bcrypt.checkpw(body['password'].encode('utf-8'), bytes(user.serialize_auth['password'], 'utf-8'))):
                role = Role.query.filter_by(id=user.role).first().serialize
                car = None
                if(user.car):
                    car = Car.query.filter_by(id=user.role).first().serialize
                user_serialize = user.serialize
                user_serialize['role'] = role['role']
                user_serialize['car'] = car

                token = jwt.encode({'user': user_serialize, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)}, 'Bearer')
                return jsonify({'user': user_serialize, 'token': token }), 200
            raise
        except:
            return jsonify({'message': 'Email or password is incorrect'}), 401

    @staticmethod
    def addUser():
        body = request.get_json()
        password_salt = bcrypt.hashpw(body['password'].encode('utf-8'), bcrypt.gensalt(10))
        user = User(body['imageProfile'], body['firstname'], body['lastname'], body['email'], password_salt, role=1, car=None)
        try:
            db.session.add(user)
            db.session.commit()
        except:
            return jsonify({'message': 'This email address is already existed'}), 404
        return jsonify({'message': 'The user information is created successfully'})

    @staticmethod
    def updateUserById(user_id):
        return db

    @staticmethod
    def deleteById(user_id):
        return db

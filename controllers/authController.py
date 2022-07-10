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
            user = User.query.filter_by(email=body['email'].lower()).first()
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
        # NOTE: body contain imageProfile, firstname, lastname, and email
        body = request.get_json()
        password_salt = bcrypt.hashpw(body['password'].encode('utf-8'), bcrypt.gensalt(10))
        user = User(body['imageProfile'], body['firstname'], body['lastname'], body['email'].lower(), password_salt, role=1, car=None)
        try:
            db.session.add(user)
            db.session.commit()
        except:
            return jsonify({'message': 'This email address is already existed'}), 404
        return jsonify({'message': 'The user information is created successfully'})

    @staticmethod
    def updateUserById(user_id):
        user = db.session.query(User).filter_by(id=user_id).first()
        try:
            if (user == None):
                return jsonify({'message': 'The user id {} is not existed'.format(user_id)}), 404
            # NOTE: can update imageProfile, email, firstname, lastname, and car
            user.imageProfile = request.get_json()['imageProfile']
            user.email = request.get_json()['email']
            user.firstname = request.get_json()['firstname']
            user.lastname = request.get_json()['lastname']
            user.car = request.get_json()['car']
            db.session.commit()
            return jsonify(user.serialize)
        except:
            return jsonify({'message': 'This email is already taken'}), 400

    @staticmethod
    def updatePasswordByUserId(user_id):
        # NOTE: body contain password
        body = request.get_json()
        user = db.session.query(User).filter_by(id=user_id).first()
        if (bcrypt.checkpw(body['oldPassword'].encode('utf-8'), bytes(user.serialize_auth['password'], 'utf-8'))):
            password_salt = bcrypt.hashpw(body['newPassword'].encode('utf-8'), bcrypt.gensalt(10))
            user.password = password_salt
            db.session.commit()
            return jsonify({'message': 'The password change successfully'}), 400
        return jsonify({'message': 'The current password is match'}), 400

    @staticmethod
    def checkEmailExist():
        # NOTE: body contain email
        body = request.get_json()
        try:
            user = User.query.filter_by(email=body['email']).first()
            if(user):
                return jsonify({'email': user.serialize['email']})
            return jsonify({'message': 'The email is available'})
        except:
            return jsonify({'message': 'The body required email'}), 400

    @staticmethod
    def deleteById(user_id):
        return db

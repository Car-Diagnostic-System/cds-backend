import datetime
import jwt
from flask import request, jsonify
import bcrypt
from models.user import User
from models.role import Role
from models.car import Car
from flask_sqlalchemy import SQLAlchemy
from utils.token import Token

db = SQLAlchemy()

class AuthController:
    @staticmethod
    def createAuthToken():
        try:
            # NOTE: body contain email and password
            email = request.get_json()['email'].lower()
            password = request.get_json()['password']
            if (not email or not password):
                return jsonify({'message': 'The email, and password cannot be null'}), 400
            try:
                user = User.query.filter_by(email=email).first()
                if (bcrypt.checkpw(password.encode('utf-8'), bytes(user.password, 'utf-8'))):
                    role = Role.query.filter_by(id=user.role).first().serialize
                    car = None
                    if(user.car):
                        car = Car.query.filter_by(id=user.car).first().serialize
                    user_serialize = user.serialize
                    user_serialize['role'] = role['role']
                    user_serialize['car'] = car
                    token = jwt.encode({'user': user_serialize, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)}, 'Bearer')
                    return jsonify({'user': user_serialize, 'token': token }), 200
                raise
            except:
                return jsonify({'message': 'Email or password is incorrect'}), 401
        except:
            return jsonify({'message': 'The request body required email, password, and car'}), 400

    @staticmethod
    def addUser():
        try:
            # NOTE: body contain imageProfile, firstname, lastname, email, and password
            imageProfile = request.get_json()['imageProfile']
            firstname = request.get_json()['firstname']
            lastname = request.get_json()['lastname']
            email = request.get_json()['email'].lower()
            password = request.get_json()['password']
            car = request.get_json()['car']
            if(not firstname or not lastname or not email or not password):
                return jsonify({'message': 'The firstname, lastname, email, and password cannot be null'}), 400
            password_salt = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))
            user = User(imageProfile, firstname, lastname, email, password_salt, role=1, car=car)
            try:
                db.session.add(user)
                db.session.commit()
            except:
                return jsonify({'message': 'This email address is already existed'}), 400
            return jsonify({'message': 'The user information is created successfully'})
        except:
            return jsonify({'message': 'The request body required imageProfile, firstname, lastname, email, password, and car'}), 400

    @staticmethod
    @Token.token_required
    def updateInfoByUserId():
        try:
            userId = request.get_json()['userId']
            imageProfile = request.get_json()['imageProfile']
            email = request.get_json()['email']
            firstname = request.get_json()['firstname']
            lastname = request.get_json()['lastname']
            car = request.get_json()['car']
            if (not firstname or not lastname or not email or not userId):
                return jsonify({'message': 'The firstname, lastname, email, and password cannot be null'}), 400
            user = db.session.query(User).filter_by(id=userId).first()
            try:
                if (user == None):
                    return jsonify({'message': 'The user id {} is not existed'.format(userId)}), 404
                # NOTE: can update imageProfile, email, firstname, lastname, and car
                user.imageProfile = imageProfile
                user.email = email
                user.firstname = firstname
                user.lastname = lastname
                user.car = car
                db.session.commit()

                role = Role.query.filter_by(id=user.role).first().serialize
                car = None
                if (user.car):
                    car = Car.query.filter_by(id=user.car).first().serialize
                user.car = car
                user.role = role['role']
                return jsonify(user.serialize)
            except:
                return jsonify({'message': 'This email is already taken'}), 400
        except:
            return jsonify({'message': 'The request body required userId, imageProfile, firstname, lastname, email, and car'}), 400

    @staticmethod
    @Token.token_required
    def updatePasswordByUserId():
        try:
            # NOTE: body contain userId, oldPassword, and newPassword
            userId = request.get_json()['userId']
            oldPassword = request.get_json()['oldPassword']
            newPassword = request.get_json()['newPassword']

            if (not userId or not oldPassword or not newPassword):
                return jsonify({'message': 'The userId, oldPassword, and newPassword cannot be null'}), 400

            user = db.session.query(User).filter_by(id=userId).first()
            if (bcrypt.checkpw(oldPassword.encode('utf-8'), bytes(user.password, 'utf-8'))):
                password_salt = bcrypt.hashpw(newPassword.encode('utf-8'), bcrypt.gensalt(10))
                user.password = password_salt
                db.session.commit()
                return jsonify({'message': 'The password is changed successfully'}), 200
            return jsonify({'message': 'The current password is not match'}), 400
        except:
            return jsonify({'message': 'The request body required userId, oldPassword, and newPassword'}), 400

    @staticmethod
    def checkEmailExist():
        try:
            # NOTE: body contain email
            email = request.get_json()['email']
            if(not email):
                return jsonify({'message': 'The email cannot be null'}), 400
            user = User.query.filter_by(email=email).first()
            if(user):
                return jsonify({'email': user.email})
            return jsonify({'email': None})
        except:
            return jsonify({'message': 'The email is required'}), 400
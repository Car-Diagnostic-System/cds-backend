from flask import request, jsonify
import jwt
from functools import wraps

class Token:
    @staticmethod
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'Token is missing'}), 403
            try:
                data = jwt.decode(token, 'Bearer', algorithms=['HS256'])
            except:
                return jsonify({'message': 'Token is invalid'}), 403
            return f(*args, **kwargs)

        return decorated

    @staticmethod
    def admin_token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'Token is missing'}), 403
            try:
                data = jwt.decode(token, 'Bearer', algorithms=['HS256'])
                if data['user']['role'] != 'ADMIN':
                    raise
            except:
                return jsonify({'message': 'Token is invalid'}), 403
            return f(*args, **kwargs)
        return decorated

    @staticmethod
    def member_token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'Token is missing'}), 403
            try:
                data = jwt.decode(token, 'Bearer', algorithms=['HS256'])
                if data['user']['role'] != 'MEMBER':
                    raise
            except:
                return jsonify({'message': 'Token is invalid'}), 403
            return f(*args, **kwargs)

        return decorated



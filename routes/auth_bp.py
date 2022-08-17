from flask import Blueprint
from controllers.authController import AuthController

class AuthBlueprint:
    auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')
    auth_bp.route('/', methods=['POST'])(AuthController.createAuthToken)
    auth_bp.route('/register', methods=['POST'])(AuthController.addUser)
    auth_bp.route('/update-information', methods=['POST'])(AuthController.updateInfoByUserId)
    auth_bp.route('/update-password', methods=['POST'])(AuthController.updatePasswordByUserId)
    auth_bp.route('/check-email', methods=['POST'])(AuthController.checkEmailExist)

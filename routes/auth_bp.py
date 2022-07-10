from flask import Blueprint

from controllers.authController import AuthController

class AuthBlueprint:
    auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')
    auth_bp.route('/', methods=['POST'])(AuthController.createAuthenticationToken)
    auth_bp.route('/register', methods=['POST'])(AuthController.addUser)
    auth_bp.route('/<int:user_id>/update', methods=['POST'])(AuthController.updateUserById)
    auth_bp.route('/<int:user_id>/update-password', methods=['POST'])(AuthController.updatePasswordByUserId)
    auth_bp.route('/check-email', methods=['POST'])(AuthController.checkEmailExist)
    auth_bp.route('/<int:user_id>/delete', methods=['DELETE'])(AuthController.deleteById)
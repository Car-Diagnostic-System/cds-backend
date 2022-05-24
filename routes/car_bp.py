from flask import Blueprint

from controllers.carController import create, getAll, getById, updateById, deleteById

car_bp = Blueprint('car_bp', __name__, url_prefix='/cars')

car_bp.route('/create', methods=['POST'])(create)
car_bp.route('/', methods=['GET'])(getAll)
car_bp.route('/<int:car_id>', methods=['GET'])(getById)
car_bp.route('/<int:car_id>/edit', methods=['POST'])(updateById)
car_bp.route('/<int:car_id>/delete', methods=['DELETE'])(deleteById)
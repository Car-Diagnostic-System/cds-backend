from flask import Blueprint

from controllers.carController import createCar, getAllCar, getAllCarPagination, getCarById, updateCarById, deleteCarById

car_bp = Blueprint('car_bp', __name__, url_prefix='/cars')

car_bp.route('/create', methods=['POST'])(createCar)
car_bp.route('/', methods=['GET'])(getAllCar)
car_bp.route('/page/<int:page>', methods=['GET'])(getAllCarPagination)
car_bp.route('/<int:car_id>', methods=['GET'])(getCarById)
car_bp.route('/<int:car_id>/edit', methods=['POST'])(updateCarById)
car_bp.route('/<int:car_id>/delete', methods=['DELETE'])(deleteCarById)
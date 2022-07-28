from flask import Blueprint
from controllers.carController import CarController

class CarBlueprint:
    car_bp = Blueprint('car_bp', __name__, url_prefix='/cars')
    # NOTE: unused endpoint
    car_bp.route('/create', methods=['POST'])(CarController.createCar)
    car_bp.route('/', methods=['GET'])(CarController.getAllCar)
    # NOTE: unused endpoint
    car_bp.route('/page/<int:page>', methods=['GET'])(CarController.getAllCarPagination)
    car_bp.route('/<int:car_id>', methods=['POST'])(CarController.getCarById)
    car_bp.route('/<int:car_id>/update', methods=['POST'])(CarController.updateCarById)
    car_bp.route('/<int:car_id>/delete', methods=['DELETE'])(CarController.deleteCarById)
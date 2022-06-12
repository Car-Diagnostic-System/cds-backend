from flask import Blueprint

from controllers.carController import CarController

class CarBlueprint:
    car_bp = Blueprint('car_bp', __name__, url_prefix='/cars')
    car_bp.route('/create', methods=['POST'])(CarController.createCar)
    car_bp.route('/', methods=['GET'])(CarController.getAllCar)
    car_bp.route('/page/<int:page>', methods=['GET'])(CarController.getAllCarPagination)
    car_bp.route('/<int:car_id>', methods=['GET'])(CarController.getCarById)
    car_bp.route('/<int:car_id>/edit', methods=['POST'])(CarController.updateCarById)
    car_bp.route('/<int:car_id>/delete', methods=['DELETE'])(CarController.deleteCarById)
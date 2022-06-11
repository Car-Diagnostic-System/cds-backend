from flask import Blueprint

from controllers.carController import carController

class CarBlueprint:
    car_bp = Blueprint('car_bp', __name__, url_prefix='/cars')
    car_bp.route('/create', methods=['POST'])(carController.createCar)
    car_bp.route('/', methods=['GET'])(carController.getAllCar)
    car_bp.route('/page/<int:page>', methods=['GET'])(carController.getAllCarPagination)
    car_bp.route('/<int:car_id>', methods=['GET'])(carController.getCarById)
    car_bp.route('/<int:car_id>/edit', methods=['POST'])(carController.updateCarById)
    car_bp.route('/<int:car_id>/delete', methods=['DELETE'])(carController.deleteCarById)
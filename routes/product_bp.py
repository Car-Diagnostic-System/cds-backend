from flask import Blueprint

from controllers.productController import create, getById, updateById , deleteById, querySymptom

product_bp = Blueprint('symptom_bp', __name__, url_prefix='/products')

product_bp.route('/create', methods=['POST'])(create)
product_bp.route('/<int:product_id>', methods=['GET'])(getById)
product_bp.route('/<int:product_id>/edit', methods=['POST'])(updateById)
product_bp.route('/<int:product_id>/delete', methods=['DELETE'])(deleteById)
product_bp.route('/query-symptom', methods=['POST'])(querySymptom)






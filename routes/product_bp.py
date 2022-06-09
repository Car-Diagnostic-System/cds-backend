from flask import Blueprint

from controllers.productController import createProduct, getAllProduct, getAllProductPagination, getProductById, updateProductById , deleteProductById

product_bp = Blueprint('product_bp', __name__, url_prefix='/products')

product_bp.route('/create', methods=['POST'])(createProduct)
product_bp.route('/', methods=['GET'])(getAllProduct)
product_bp.route('/page/<int:page>', methods=['GET'])(getAllProductPagination)
product_bp.route('/<string:product_id>', methods=['GET'])(getProductById)
product_bp.route('/<string:product_id>/edit', methods=['POST'])(updateProductById)
product_bp.route('/<string:product_id>/delete', methods=['DELETE'])(deleteProductById)

from flask import Blueprint
from controllers.productController import ProductController

class ProductBlueprint:
    product_bp = Blueprint('product_bp', __name__, url_prefix='/products')
    product_bp.route('/create', methods=['POST'])(ProductController.createProduct)
    product_bp.route('/', methods=['GET'])(ProductController.getAllProduct)
    product_bp.route('/page/<int:page>', methods=['GET'])(ProductController.getAllProductPagination)
    product_bp.route('/<string:product_id>', methods=['GET'])(ProductController.getProductById)
    product_bp.route('/<string:product_id>/edit', methods=['POST'])(ProductController.updateProductById)
    product_bp.route('/<string:product_id>/delete', methods=['DELETE'])(ProductController.deleteProductById)

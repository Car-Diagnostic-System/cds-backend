from flask import Blueprint
from controllers.bucketController import BucketController

class BucketBlueprint:
    bucket_bp = Blueprint('bucket_bp', __name__, url_prefix='/bucket')
    bucket_bp.route('/uploadFile', methods=['POST'])(BucketController.uploadFile)

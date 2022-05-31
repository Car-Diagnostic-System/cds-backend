from flask import Blueprint

from controllers.symptomController import query, indexing

symptom_bp = Blueprint('symptom_bp', __name__, url_prefix='/symptom')

symptom_bp.route('/query', methods=['POST'])(query)
symptom_bp.route('/indexing', methods=['POST'])(indexing)

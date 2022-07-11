from flask import Blueprint
from controllers.symptomController import SymptomController

class SymptomBlueprint:
    symptom_bp = Blueprint('symptom_bp', __name__, url_prefix='/symptom')
    symptom_bp.route('/query', methods=['POST'])(SymptomController.queryCarSymptom)
    symptom_bp.route('/indexing', methods=['POST'])(SymptomController.indexing)

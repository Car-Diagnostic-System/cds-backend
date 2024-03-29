from flask import Flask
from flask_cors import CORS
from sqlalchemy_utils.functions import database_exists, create_database
from routes.auth_bp import AuthBlueprint
from routes.car_bp import CarBlueprint
from routes.product_bp import ProductBlueprint
from routes.symptom_bp import SymptomBlueprint
from routes.bookmark_bp import BookmarkBlueprint
from routes.bucket_bp import BucketBlueprint
from models.database import db

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
app.config.from_object('config')

if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    print('Creating a database')
    create_database(app.config["SQLALCHEMY_DATABASE_URI"])

db.init_app(app)
with app.app_context():
    db.create_all()

class FlaskApp:
    app.register_blueprint(AuthBlueprint.auth_bp)
    app.register_blueprint(CarBlueprint.car_bp)
    app.register_blueprint(ProductBlueprint.product_bp)
    app.register_blueprint(SymptomBlueprint.symptom_bp)
    app.register_blueprint(BookmarkBlueprint.bookmark_bp)
    app.register_blueprint(BucketBlueprint.bucket_bp)

if __name__ == '__main__':
    app.run()

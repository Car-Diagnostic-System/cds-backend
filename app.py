from flask import Flask
from flask_cors import CORS

from sqlalchemy_utils.functions import database_exists, create_database
from routes.user_bp import user_bp
from routes.car_bp import car_bp
from routes.product_bp import product_bp
from models.database import db

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

app.config.from_object('config')

if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    print('Create a database')
    create_database(app.config["SQLALCHEMY_DATABASE_URI"])

db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(user_bp)
app.register_blueprint(car_bp)
app.register_blueprint(product_bp)


if __name__ == '__main__':
    app.run()

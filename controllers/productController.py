from flask import jsonify, request
from models.products import Product
from kafka import KafkaConsumer, KafkaProducer
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

# Kafka config
TOPIC_NAME = 'INFERENCE'
KAFKA_SERVER = 'localhost:9092'

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    api_version=(0, 11, 15)
)

def create():
    body = request.get_json()
    product = Product(body['serial_no'], body['supplier_no'], body['oem_no'], body['benchmark_no'], body['car_brand'], body['car_model'], body['model_name_th'],
                      body['nickname'], body['item_name'], body['fitment_detail'], body['brand'], body['item_group'], body['stock_uom'],)
    try:
        db.session.add(product)
        db.session.commit()
    except:
        return jsonify({'error': 'This product information is already existed'}), 404

    return jsonify({'message': 'The product information is created successfully'})

def getById(product_id):
    product = Product.query.filter_by(serial_no=product_id).first()
    if(product == None):
        return jsonify({'error': 'The product id {} is not existed'.format(product_id)}), 404
    return jsonify(product.serialize)

def updateById(product_id):
    product = Product.query.filter_by(serial_no=product_id).first()
    if (product == None):
        return jsonify({'error': 'The product id {} is not existed'.format(product_id)}), 404
    product.supplier_no = request.get_json()['supplier_no']
    product.oem_no = request.get_json()['oem_no']
    product.benchmark_no = request.get_json()['benchmark_no']
    product.car_brand = request.get_json()['car_brand']
    product.car_model = request.get_json()['car_model']
    product.model_name_th = request.get_json()['model_name_th']
    product.nickname = request.get_json()['nickname']
    product.item_name = request.get_json()['item_name']
    product.fitment_detail = request.get_json()['fitment_detail']
    product.brand = request.get_json()['brand']
    product.item_group = request.get_json()['item_group']
    product.stock_uom = request.get_json()['stock_uom']
    print(product)
    db.session.commit()
    return jsonify(product.serialize)

def deleteById(product_id):
    car = db.session.get(Product, product_id)
    try:
        db.session.delete(car)
        db.session.commit()
    except:
        return jsonify({'error': 'The product id {} is not existed'.format(product_id)}), 404
    return jsonify({'message': 'The car product {} is deleted successfully'.format(product_id)})

def querySymptom():
    body = request.get_json()

    # Kafka produce
    json_payload = json.dumps(body['symptom'])
    json_payload = str.encode(json_payload)

    producer.send(TOPIC_NAME, json_payload)
    producer.flush()

    product = Product.query.filter(((Product.car_brand == body['brand']) | (Product.car_brand == "")) &
                                   ((Product.car_model == body['model']) | (Product.car_model == "")) &
                                   ((Product.nickname == body['nickname']) | (Product.nickname == "")))
    product = Product.serialize_list(product)
    if(len(product) == 0):
        return jsonify({'error': 'The product is not found'}), 404
    return jsonify(product)

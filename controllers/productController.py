from time import sleep

from flask import jsonify, request
from models.products import Product
from kafka import KafkaConsumer, KafkaProducer, TopicPartition
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()
CONSUMER_TOPIC_NAME = "QUERY-RESPONSE"
PRODUCER_TOPIC_NAME = 'QUERY'
KAFKA_SERVER = 'localhost:9092'

consumer = KafkaConsumer(
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
)

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

def getAll():
    products = Product.query.all()
    products = Product.serialize_list(products)
    return jsonify(products)

def getAllPagination(page=1):
    perPage = 10
    products = Product.query.paginate(page=page, per_page=perPage, error_out=False)
    totalPage = products.pages
    hasNext = products.has_next
    hasPrev = products.has_prev
    nextPage = products.next_num
    prevPage = products.prev_num
    products = Product.serialize_list(products.items)
    return jsonify({'currentPage': page, 'totalPage': totalPage, 'hasNext':hasNext, 'hasPrev': hasPrev, 'nextPage':nextPage, 'prevPage':prevPage, 'data': products})

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
    json_payload = json.dumps(body)
    json_payload = str.encode(json_payload)

    producer.send(PRODUCER_TOPIC_NAME, json_payload)
    producer.flush()
    sleep(0.05)
    # Kafka consume
    tp = TopicPartition(CONSUMER_TOPIC_NAME, 0)
    consumer.assign([tp])
    consumer.seek_to_end(tp)
    lastOffSet = consumer.position(tp)
    consumer.seek_to_beginning(tp)
    parts = {}

    for msg in consumer:
        if(msg.offset == lastOffSet -1):
            parts = msg.value
            break
    product = Product.query.filter(((Product.car_brand == body['brand']) | (Product.car_brand == "")) &
                                   ((Product.car_model == body['model']) | (Product.car_model == "")) &
                                   ((Product.nickname == body['nickname']) | (Product.nickname == "")))
    product = Product.serialize_list(product)
    result = []
    for p in parts.items():
        obj = {
            'part': p[0],
            'score': p[1],
            'product': list(filter(lambda s: s['item_name'] == p[0], product))
        }
        result.append(obj)

    if(len(product) == 0):
        return jsonify({'error': 'The product is not found'}), 404
    
    return jsonify(result)


# [
#     {
#         'name': 'โบลเวอร์',
#         'products': [
#             {'serial_no': 'AA-0000603', 'supplier_no': 'C1N020', 'oem_no': '45022-SEL-T02', 'benchmark_no': '', 'car_brand': 'HONDA', 'car_model': 'JAZZ', 'model_name_th': 'แจ๊ส', 'nickname': '', 'item_name': 'ผ้าดิสเบรค', 'fitment_detail': 'หน้า', 'brand': 'ADVICS', 'item_group': 'เทียบแท้เกรด A', 'stock_uom': 'ชิ้น'},
#             {'serial_no': 'AA-0000603', 'supplier_no': 'C1N020', 'oem_no': '45022-SEL-T02', 'benchmark_no': '', 'car_brand': 'HONDA', 'car_model': 'JAZZ', 'model_name_th': 'แจ๊ส', 'nickname': '', 'item_name': 'ผ้าดิสเบรค', 'fitment_detail': 'หน้า', 'brand': 'ADVICS', 'item_group': 'เทียบแท้เกรด A', 'stock_uom': 'ชิ้น'}
#         ]
#     }
# ]

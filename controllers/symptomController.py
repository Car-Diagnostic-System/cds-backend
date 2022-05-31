import json
from time import sleep
import pandas as pd
from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy
from kafka import KafkaConsumer, KafkaProducer, TopicPartition

from models.products import Product

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

def query():
    body = request.get_json()

    # Kafka produce
    json_payload = json.dumps(body)
    json_payload = str.encode(json_payload)

    producer.send(PRODUCER_TOPIC_NAME, json_payload)
    producer.flush()
    sleep(1)
    # Kafka consume
    tp = TopicPartition(CONSUMER_TOPIC_NAME, 0)
    consumer.assign([tp])
    consumer.seek_to_end(tp)
    lastOffSet = consumer.position(tp)
    consumer.seek_to_beginning(tp)
    parts = {}

    for msg in consumer:
        if (msg.offset == lastOffSet - 1):
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

    if (len(product) == 0):
        return jsonify({'error': 'The product is not found'}), 404

    return jsonify(result)


def indexing():
    if 'file' not in request.files:
        return jsonify({'error': 'No file is not exist'})
    file = request.files['file']
    if file.filename.split('.')[-1].lower() != 'xlsx':
        return jsonify({'error': 'Require xlsx file format'})
    df = pd.read_excel(file)
    if(len(df.columns) != 2):
        return jsonify({'error': 'Require only two columns of xlsx file'})
    if (len(df.index) == 0):
        return jsonify({'error': 'The xlsx is empty'})

    # send along with kafka INDEX topic
    json_payload = df.to_json()
    json_payload = str.encode(json_payload)

    producer.send('INDEX', json_payload)
    producer.flush()

    return jsonify({'message': 'Upload indexing file successfully'})
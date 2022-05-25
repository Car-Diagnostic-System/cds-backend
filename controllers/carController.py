from models.car import Car
from flask import jsonify, request

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def create():
    body = request.get_json()
    car = Car(body['brand'], body['model'], body['nickname'])
    try:
        db.session.add(car)
        db.session.commit()
    except:
        return jsonify({'error': 'This car information is already existed'}), 404

    return jsonify({'message': 'The car information is created successfully'})

def getAll():
    cars = Car.query.all()
    cars = Car.serialize_list(cars)
    result = {m['brand']: [] for m in cars}
    for m in cars:
        result[m['brand']].append({'id': m['id'], 'model': m['model'], 'model_th': m['model_th'], 'nickname': m['nickname']})
    return jsonify(result)

def getAllPagination(page=1):
    perPage = 10
    cars = Car.query.paginate(page=page, per_page=perPage, error_out=False)
    totalPage = cars.pages
    hasNext = cars.has_next
    hasPrev = cars.has_prev
    nextPage = cars.next_num
    prevPage = cars.prev_num
    cars = Car.serialize_list(cars.items)
    return jsonify({'currentPage': page, 'totalPage': totalPage, 'hasNext':hasNext, 'hasPrev': hasPrev, 'nextPage':nextPage, 'prevPage':prevPage, 'data': cars})

def getById(car_id):
    car = Car.query.get(car_id)
    if (car == None):
        return jsonify({'error': 'The car id {} is not existed'.format(car_id)}), 404
    return jsonify(car.serialize)

def updateById(car_id):
    car = Car.query.get(car_id)
    if (car == None):
        return jsonify({'error': 'The car id {} is not existed'.format(car_id)}), 404
    car.brand = request.get_json()['brand']
    car.model = request.get_json()['model']
    car.nickname = request.get_json()['nickname']
    db.session.commit()
    return jsonify(car.serialize)

def deleteById(car_id):
    car = db.session.get(Car, car_id)
    try:
        db.session.delete(car)
        db.session.commit()
    except:
        return jsonify({'error': 'The car id {} is not existed'.format(car_id)}), 404

    return jsonify({'message': 'The car id {} is deleted successfully'.format(car_id)})

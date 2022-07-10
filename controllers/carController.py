from models.car import Car
from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy
from controllers.token import Token
db = SQLAlchemy()

class CarController:
    @staticmethod
    def createCar():
        body = request.get_json()
        car = Car(body['brand'], body['brand_th'], body['model'], body['model_th'], body['nickname'], body['segment'])
        try:
            db.session.add(car)
            db.session.commit()
        except:
            return jsonify({'message': 'This car information is already existed'}), 404

        return jsonify({'message': 'The car information is created successfully'})

    @staticmethod
    @Token.token_required
    def getAllCar():
        cars = Car.query.all()
        cars = Car.serialize_list(cars)
        brands = tuple(set(map(lambda s: (s['brand'], s['brand_th']), cars)))
        result = []
        for car in brands:
            obj = {'brand': car[0], 'brand_th': car[1], 'model': list(filter(lambda s: s['brand'] == car[0], cars))}
            obj['model']
            result.append(obj)
        result = sorted(result, key=lambda d: d['brand'])
        return jsonify(result)

    @staticmethod
    def getAllCarPagination(page=1):
        perPage = 10
        cars = Car.query.paginate(page=page, per_page=perPage, error_out=False)
        totalPage = cars.pages
        hasNext = cars.has_next
        hasPrev = cars.has_prev
        nextPage = cars.next_num
        prevPage = cars.prev_num
        cars = Car.serialize_list(cars.items)
        return jsonify({'currentPage': page, 'totalPage': totalPage, 'hasNext':hasNext, 'hasPrev': hasPrev, 'nextPage':nextPage, 'prevPage':prevPage, 'data': cars})

    @staticmethod
    def getCarById(car_id):
        car = Car.query.get(car_id)
        if (car == None):
            return jsonify({'message': 'The car id {} is not existed'.format(car_id)}), 404
        return jsonify(car.serialize)

    @staticmethod
    def updateCarById(car_id):
        car = db.session.query(Car).filter_by(id=car_id).first()
        print(car)
        if (car == None):
            return jsonify({'message': 'The car id {} is not existed'.format(car_id)}), 404
        car.brand = request.get_json()['brand']
        car.model = request.get_json()['model']
        car.nickname = request.get_json()['nickname']
        db.session.commit()
        return jsonify(car.serialize)

    @staticmethod
    def deleteCarById(car_id):
        car = db.session.get(Car, car_id)
        try:
            db.session.delete(car)
            db.session.commit()
        except:
            return jsonify({'message': 'The car id {} is not existed'.format(car_id)}), 404

        return jsonify({'message': 'The car id {} is deleted successfully'.format(car_id)})

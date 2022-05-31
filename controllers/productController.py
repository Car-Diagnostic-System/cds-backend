from flask import jsonify, request
from models.products import Product
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

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

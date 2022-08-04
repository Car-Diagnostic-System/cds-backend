import bcrypt
from sqlalchemy import event
from .database import db
from .car import Car
from .role import Role
from .user import User
from .product import Product
from .bookmark import Bookmark
import pandas as pd

@event.listens_for(Car.__table__, 'after_create')
def create_car(*args, **kwargs):
    print('Inserting car table')
    cars = pd.read_csv('assets/cars.csv')
    for car in cars.values:
        brand = car[1] if type(car[1]) != float else ''
        brand_th = car[2] if type(car[2]) != float else ''
        model = car[3] if type(car[3]) != float else ''
        model_th = car[4] if type(car[4]) != float else ''
        nickname = car[5] if type(car[5]) != float else ''
        segment = car[6] if type(car[6]) != float else ''
        db.session.add(Car(brand=brand, brand_th=brand_th, model=model, model_th=model_th, nickname=nickname, segment=segment))
        db.session.commit()

@event.listens_for(Product.__table__, 'after_create')
def create_product(*args, **kwargs):
    print('Inserting product table')
    products = pd.read_csv('assets/products.csv')
    for product in products.values:
        serial_no = product[0] if type(product[0]) != float else ''
        supplier_no = product[1] if type(product[1]) != float else ''
        oem_no = product[2] if type(product[2]) != float else ''
        benchmark_no = product[3] if type(product[3]) != float else ''
        car_brand = product[4] if type(product[4]) != float else ''
        car_model = product[5] if type(product[5]) != float else ''
        model_name_th = product[6] if type(product[6]) != float else ''
        nickname = product[7] if type(product[7]) != float else ''
        item_name = product[8] if type(product[8]) != float else ''
        fitment_detail = product[9] if type(product[9]) != float else ''
        brand = product[10] if type(product[10]) != float else ''
        item_group = product[11] if type(product[11]) != float else ''
        stock_uom = product[12] if type(product[12]) != float else ''
        db.session.add(Product(serial_no=serial_no, supplier_no=supplier_no, oem_no=oem_no, benchmark_no=benchmark_no, car_brand=car_brand, car_model=car_model, model_name_th=model_name_th,
                               nickname=nickname, item_name=item_name, fitment_detail=fitment_detail, brand=brand, item_group=item_group, stock_uom=stock_uom))
        db.session.commit()

@event.listens_for(Role.__table__, 'after_create')
def create_role(*args, **kwargs):
    print('Inserting role table')
    db.session.add(Role('MEMBER'))
    db.session.add(Role('ADMIN'))
    db.session.commit()

@event.listens_for(User.__table__, 'after_create')
def create_user(*args, **kwargs):
    print('Inserting user table')
    db.session.add(User(imageProfile='https://cds-photo.s3.ap-southeast-1.amazonaws.com/kaismile.PNG', firstname='ตุลยวัต', lastname='ทับคง', email='tulyawatt@gmail.com', password=bcrypt.hashpw('kaiPassword'.encode('utf-8'), bcrypt.gensalt(10)), role=2, car=None))
    db.session.add(User(imageProfile='https://cds-photo.s3.ap-southeast-1.amazonaws.com/tong.jpeg', firstname='กฤตพร', lastname='แก้วปิยรัตน์', email='krittaporn.tong@gmail.com', password=bcrypt.hashpw('tongPassword'.encode('utf-8'), bcrypt.gensalt(10)), role=1, car=1016))
    db.session.add(User(imageProfile='https://cds-photo.s3.ap-southeast-1.amazonaws.com/fax.jpeg', firstname='พรมงคง', lastname='พุทธิแจ่ม', email='fax@gmail.com', password=bcrypt.hashpw('faxPassword'.encode('utf-8'), bcrypt.gensalt(10)), role=1, car=322))
    db.session.add(User(imageProfile='https://cds-photo.s3.ap-southeast-1.amazonaws.com/kong.jpeg', firstname='ภาสกร', lastname='เปียงใจ', email='kong@gmail.com', password=bcrypt.hashpw('kongPassword'.encode('utf-8'), bcrypt.gensalt(10)), role=1, car=921))
    db.session.commit()

@event.listens_for(Bookmark.__table__, 'after_create')
def create_bookmark(*args, **kwargs):
    print('Inserting bookmark table')
    db.session.add(Bookmark(user=4, product='CA-0000921'))
    db.session.add(Bookmark(user=4, product='DD-0400061'))
    db.session.add(Bookmark(user=4, product='DF-0700874'))
    db.session.commit()

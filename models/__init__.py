import bcrypt
from sqlalchemy import event
from sqlalchemy import DDL

from models.database import db
from models.role import Role
from models.user import User

@event.listens_for(Role.__table__, 'after_create')
def create_roles(*args, **kwargs):
    db.session.add(Role('USER'))
    db.session.add(Role('ADMIN'))
    db.session.commit()

@event.listens_for(User.__table__, 'after_create')
def create_users(*args, **kwargs):
    db.session.add(User(imageProfile='image.png', firstname='ตุลยวัต', lastname='ทับคง', email='tulyawatt@gmail.com', password=bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt(10)), role=2, car=None))
    db.session.add(User(imageProfile='image.png', firstname='กฤตพร', lastname='แก้วปิยรัตน์', email='krittaporn.tong@gmail.com', password=bcrypt.hashpw('1234'.encode('utf-8'), bcrypt.gensalt(10)), role=1, car=1016))
    db.session.add(User(imageProfile='image.png', firstname='พรมงคง', lastname='พุทธิแจ่ม', email='fax@gmail.com', password=bcrypt.hashpw('faxpassword'.encode('utf-8'), bcrypt.gensalt(10)), role=1, car=322))
    db.session.add(User(imageProfile='image.png', firstname='ภาสกร', lastname='เปียงใจ', email='kong@gmail.com', password=bcrypt.hashpw('kongpassword'.encode('utf-8'), bcrypt.gensalt(10)), role=1, car=921))
    db.session.commit()

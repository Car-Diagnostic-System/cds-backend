from .database import db

class Car(db.Model):
    __tablename__ = 'car'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(255))
    brand_th = db.Column(db.String(255))
    model = db.Column(db.String(255))
    model_th = db.Column(db.String(255))
    nickname = db.Column(db.String(255))
    segment = db.Column(db.String(255))
    user = db.relationship('User', backref='Car', lazy=True)


    def __init__(self, brand, brand_th, model, model_th, nickname, segment):
        self.brand = brand
        self.brand_th = brand_th
        self.model = model
        self.model_th = model_th
        self.nickname = nickname
        self.segment = segment

    @property
    def serialize(self):
        return {
            'id': self.id,
            'brand': self.brand,
            'brand_th': self.brand_th,
            'model': self.model,
            'model_th': self.model_th,
            'nickname': self.nickname,
            'segment': self.segment,
        }

    @staticmethod
    def serialize_list(list):
        return [m.serialize for m in list]
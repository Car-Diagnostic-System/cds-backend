from .database import db

class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(255))
    model = db.Column(db.String(255))
    model_th = db.Column(db.String(255))

    nickname = db.Column(db.String(255))
    __table_args__ = (db.UniqueConstraint('brand', 'model', 'nickname'),
                      )
    def __init__(self, brand, model,model_th, nickname):
        self.brand = brand
        self.model = model
        self.model_th = model_th
        self.nickname = nickname

    @property
    def serialize(self):
        return {
            'id': self.id,
            'brand': self.brand,
            'model': self.model,
            'model_th': self.model_th,
            'nickname': self.nickname,
        }

    @staticmethod
    def serialize_list(l):
        return [m.serialize for m in l]
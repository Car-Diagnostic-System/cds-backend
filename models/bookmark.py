from .database import db

class Bookmark(db.Model):
    __tablename__ = 'bookmark'
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    product = db.Column(db.String(255), db.ForeignKey('product.serial_no'), nullable=False, primary_key=True)

    def __init__(self, user, product):
        self.user = user
        self.product = product

    @property
    def serialize(self):
        return {
            'user': self.user,
            'product': self.product,
        }

    @staticmethod
    def serialize_list(list):
        return [m.serialize for m in list]
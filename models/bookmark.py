from .database import db

class Bookmark(db.Model):
    __tablename__ = 'bookmark'
    id = db.Column(db.Integer, primary_key=True)
    #
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    # user = db.relationship("User", backref=db.backref("user", uselist=False))
    #
    # product_serial_no = db.Column(db.String(255), db.ForeignKey('products.serial_no'), primary_key=True)
    # product = db.relationship("Product", backref=db.backref("product", uselist=False))

    @property
    def serialize(self):
        return {
            'id': self.id
            # 'user_id': self.user_id,
            # 'product_serial_no': self.product_serial_no
         }
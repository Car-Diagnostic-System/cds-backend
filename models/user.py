from .database import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    imageProfile = db.Column(db.String(255), nullable=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    # car_id = db.Column(db.Integer, db.ForeignKey('my_schema.cars.id'))
    # car = db.relationship("Car", backref=db.backref("car", uselist=False))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'imageProfile': self.imageProfile,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'password': self.password,
            # 'car_id': self.car_id
        }

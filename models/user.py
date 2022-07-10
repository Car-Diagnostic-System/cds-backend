from .database import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    imageProfile = db.Column(db.String(255), nullable=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    role = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    car = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=True)

    def __init__(self, imageProfile, firstname, lastname, email, password, role, car):
        self.imageProfile = imageProfile
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.role = role
        self.car = car

    @property
    def serialize(self):
        return {
            'id': self.id,
            'imageProfile': self.imageProfile,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'role': self.role,
            'car': self.car
        }

    @property
    def serialize_auth(self):
        return {
            'email': self.email,
            'password': self.password
        }

    @staticmethod
    def serialize_list(list):
        return [m.serialize for m in list]
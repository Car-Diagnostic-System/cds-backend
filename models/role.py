from .database import db

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(255))
    user = db.relationship('User', backref='Role', lazy=True)

    def __init__(self, role):
        self.role = role

    @property
    def serialize(self):
        return {
            'role': self.role,
        }

    @staticmethod
    def serialize_list(list):
        return [m.serialize for m in list]
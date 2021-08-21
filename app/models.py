from . import db
from werkzeug.security import generate_password_hash,check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    pass_secure=db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('You cannot access password attribute')

    def __repr__(self):
        return f'User {self.username}'
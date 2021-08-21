
from operator import index

from sqlalchemy.orm import backref
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email=db.Column(db.String(255),unique=True,index=True)
    password_hash=db.Column(db.String(255))
    pass_secure=db.Column(db.String(255))
    bio=db.Column(db.String(255))
    profile_pic_path=db.Column(db.String(255))
    blogs=db.relationship('Blog',backref='user',lazy='dynamic')
    comment=db.relationship('Comment',backref='user',lazy='dynamic')


    @property
    def password(self):
        raise AttributeError('You cannot access password attribute')

    @password.setter
    def password(self,password):
        self.pass_secure=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'


class Blog(db.Model):
    __tablename__='blogs'
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(255))
    post=db.column(db.Text(),nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    blog=db.relationship('Blog',backref)


    def save_b(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Blog {self.post}'

class Comment(db.Model):
    __tablename__='comments'
    id=db.Column(db.Integer,primary_key=True)
    comment=db.Column(db.Text(),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    blog_id=db.Column(db.Integer,db.ForeignKey('blogs.id'),nullable=False)


from datetime import datetime

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import db
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class AccountTransaction(db.Model, SerializerMixin):
    __tablename__ = 'account_transaction'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False, unique=False, server_default='0')
    transaction_type = db.Column(db.String(300), nullable=True, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, amount, transaction_type, user_id):
        self.amount = amount
        self.transaction_type = transaction_type
        self.user_id = user_id


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    about = db.Column(db.String(300), nullable=True, unique=False)
    authenticated = db.Column(db.Boolean, default=False)
    registered_on = db.Column('registered_on', db.DateTime)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    is_admin = db.Column('is_admin', db.Boolean(), nullable=False, server_default='0')
    account_balance = db.Column(db.Integer, nullable=False, server_default='0')
    account_transaction = db.relationship("AccountTransaction", backref="user", cascade="all, delete")

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.email

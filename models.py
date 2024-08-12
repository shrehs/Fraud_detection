from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    address = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    credit_score = db.Column(db.Integer, default=0)

class CreditCard(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    card_number = db.Column(db.String(16), unique=True, nullable=False)
    card_limit = db.Column(db.Numeric(10, 2), nullable=False)
    credit_used = db.Column(db.Numeric(10, 2), default=0.00)
    expiry_date = db.Column(db.Date, nullable=False)
    user = db.relationship('User', backref=db.backref('credit_cards', lazy=True))

class Transaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('credit_card.card_id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(255))
    credit_card = db.relationship('CreditCard', backref=db.backref('transactions', lazy=True))

class Payment(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('credit_card.card_id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    credit_card = db.relationship('CreditCard', backref=db.backref('payments', lazy=True))
from flask import request, jsonify
from app import app, model, auth
from models import db, User, CreditCard, Transaction, Payment
from utils import calculate_credit_score
import pandas as pd
from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

@app.route('/create_user', methods=['POST'])
@auth.login_required
def create_user():
    data = request.json
    new_user = User(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        address=data['address']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/add_credit_card', methods=['POST'])
@auth.login_required
def add_credit_card():
    data = request.json
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'message': 'User not found'}), 404
    new_card = CreditCard(
        user_id=data['user_id'],
        card_number=data['card_number'],
        card_limit=data['card_limit'],
        expiry_date=data['expiry_date']
    )
    db.session.add(new_card)
    db.session.commit()
    return jsonify({'message': 'Credit card added successfully'}), 201

@app.route('/add_transaction', methods=['POST'])
@auth.login_required
def add_transaction():
    data = request.json
    card = CreditCard.query.get(data['card_id'])
    if not card:
        return jsonify({'message': 'Credit card not found'}), 404
    
    # Prepare data for fraud detection
    transaction_data = {
        'amount': [data['amount']],
        'card_id': [data['card_id']],
    }
    transaction_df = pd.DataFrame(transaction_data)
    
    # Predict fraud
    prediction = model.predict(transaction_df)[0]
    
    if prediction == 1:
        return jsonify({'message': 'Transaction flagged as fraud'}), 403
    
    new_transaction = Transaction(
        card_id=data['card_id'],
        amount=data['amount'],
        description=data['description']
    )
    card.credit_used += data['amount']
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction added successfully'}), 201

@app.route('/make_payment', methods=['POST'])
@auth.login_required
def make_payment():
    data = request.json
    card = CreditCard.query.get(data['card_id'])
    if not card:
        return jsonify({'message': 'Credit card not found'}), 404
    new_payment = Payment(
        card_id=data['card_id'],
        amount=data['amount']
    )
    card.credit_used -= data['amount']
    db.session.add(new_payment)
    db.session.commit()
    return jsonify({'message': 'Payment made successfully'}), 201

@app.route('/update_credit_score', methods=['POST'])
@auth.login_required
def update_credit_score():
    data = request.json
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user.credit_score = calculate_credit_score(user)
    db.session.commit()
    return jsonify({'message': 'Credit score updated successfully'}), 200

users = {
    "user@example.com": {"password": "password123", "name": "John Doe"}
}

def setup_routes(app):
    @app.route('/login', methods=['POST'])
    def login():
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        user = users.get(email)

        if not user or user['password'] != password:
            return jsonify({"msg": "Bad email or password"}), 401

        # Create a new token with the user id inside
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token)

    @app.route('/protected', methods=['GET'])
    @jwt_required()
    def protected():
        # Access the identity of the current user with get_jwt_identity
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user), 200
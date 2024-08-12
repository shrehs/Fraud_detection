# Credit Card System with Fraud Detection

This project implements a credit card system inspired by American Express, with features including user management, credit card management, transaction handling, payment processing, and fraud detection using a machine learning model. The backend is developed using Python and Flask, with a MySQL database to store data securely.

## Features

- **User Management**: Create and manage user profiles.
- **Credit Card Management**: Add and manage credit card details for users.
- **Transaction Handling**: Record and monitor transactions.
- **Fraud Detection**: Integrate a trained machine learning model to detect fraudulent transactions.
- **Payment Processing**: Manage and record payments towards credit card balances.
- **Security Features**: Implement basic authentication to protect API endpoints.

## Requirements

- Python 3.7 or higher
- Flask
- Flask-SQLAlchemy
- Flask-HTTPAuth
- MySQL
- scikit-learn
- pandas
- joblib
- werkzeug

## Setup and Installation

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/yourusername/credit-card-system.git
   cd credit-card-system
Create and Activate a Virtual Environment:

sh
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install Dependencies:

sh
Copy code
pip install -r requirements.txt
Set Up the MySQL Database:

Create a database named credit_card_db.
Use the provided SQL script to create tables and relationships.
Configure the Database:

Update config.py with your MySQL database credentials.
Train and Save the Fraud Detection Model:

Run train_model.py to train the model and save it as fraud_detection_model.pkl.

API Endpoints
POST /create_user: Create a new user.
POST /add_credit_card: Add a credit card to a user.
POST /add_transaction: Add a transaction with fraud detection.
POST /make_payment: Make a payment towards a credit card.
POST /update_credit_score: Update a user's credit score.
Security
Basic Authentication: Protects API endpoints. Use the admin username with password adminpass for access.
Input Validation: Ensures secure data handling and prevents SQL injection.
Fraud Detection
The fraud detection model is built using a Random Forest Classifier from scikit-learn.
To retrain the model, modify and run train_model.py with your dataset.
Additional Security Features
HTTPS: Ensure the server is configured to use HTTPS for encrypted communication.
Data Validation: Validate inputs and outputs rigorously to prevent security vulnerabilities.
Future Improvements
Front-end improvement
Implement role-based access control for finer-grained security.
Expand the dataset for training a more robust fraud detection model.
Add logging and monitoring for real-time alerts on suspicious activities.
Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

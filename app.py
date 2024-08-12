from flask import Flask
from config import Config
from models import db
import joblib
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("adminpass")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Load the fraud detection model
model = joblib.load('fraud_detection_model.pkl')

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret_key'  # Change this to a random secret key
jwt = JWTManager(app)

# Enable CORS for requests from your React app
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


with app.app_context():
    db.create_all()

from routes import setup_routes
setup_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
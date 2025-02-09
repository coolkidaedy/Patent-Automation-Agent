# app.py
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os
from extensions import db
from operations import operations

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///default.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Register the blueprint (no prefix is used here, so endpoints are at /submit, /search, etc.)
app.register_blueprint(operations)

if __name__ == '__main__':
    app.run(debug=True)

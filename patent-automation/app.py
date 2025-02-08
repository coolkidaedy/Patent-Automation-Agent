from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///default.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Patent(db.Model): 
    __tablename__ = 'patents'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(600), nullable=False)  # Removed unique constraint

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy

class User(db.model): 
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, unique = True)
    title = db.Column(db.String(255), nullable = False, unique = True)
    description = db.Column(db.String(600), nullable = False, unique = True)
    

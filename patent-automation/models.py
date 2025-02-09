# models.py
from extensions import db

class Patent(db.Model): 
    __tablename__ = 'patents'
    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)  # Increased length to accommodate large descriptions

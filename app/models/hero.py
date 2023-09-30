from datetime import datetime
from .dbconfig import db

class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    super_name = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Include created_at
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Include updated_at

    # Define the relationship with HeroPower
    hero_powers = db.relationship("HeroPower", back_populates="hero")

    def __init__(self, name, super_name):
        self.name = name
        self.super_name = super_name

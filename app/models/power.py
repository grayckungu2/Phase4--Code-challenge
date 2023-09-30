from datetime import datetime
from .dbconfig import db

class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define the relationship with HeroPower
    power_heroes = db.relationship("HeroPower", back_populates="power")

    def __init__(self, name, description):
        self.name = name
        self.description = description

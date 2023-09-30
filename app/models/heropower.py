from datetime import datetime
from .dbconfig import db

class HeroPower(db.Model):
    __tablename__ = 'hero_power'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign key relationships
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)

    # Relationships with Hero and Power models
    hero = db.relationship("Hero", back_populates="hero_powers")
    power = db.relationship("Power", back_populates="power_heroes")

    def __init__(self, strength, hero, power):
        self.strength = strength
        self.hero = hero
        self.power = power

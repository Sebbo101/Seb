from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(255), nullable=False)
    airline = db.Column(db.String(255), nullable=False)
    registration = db.Column(db.String(255), nullable=False)
    departure_airport = db.Column(db.String(255), nullable=False)
    arrival_airport = db.Column(db.String(255), nullable=False)
    aircraft_type = db.Column(db.String(255), nullable=False)
    departure_delay = db.Column(db.Integer, nullable=False)
    aircraft_cleanliness = db.Column(db.Integer, nullable=False)
    friendliness = db.Column(db.Integer, nullable=False)
    entertainment_quality = db.Column(db.Integer, nullable=False)
    food_quality = db.Column(db.Integer, nullable=False)
    user_friendliness = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
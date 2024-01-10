from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.String(255), nullable=False)
    flight_number = db.Column(db.String(255), nullable=False)
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

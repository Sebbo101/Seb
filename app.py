from flask import Flask, render_template,request, redirect, url_for
from flask_migrate import Migrate
from models import db, Review

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'  # SQLite-database bestand
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    reviews = Review.query.all()
    return render_template('index.html', reviews=reviews)

@app.route('/add_review', methods=['GET', 'POST'])
def add_review():
    if request.method == 'POST':
        airline = request.form.get('airline')
        flight_number = request.form.get('flight_number')
        registration = request.form.get('registration')
        departure_airport = request.form.get('departure_airport')
        arrival_airport = request.form.get('arrival_airport')
        aircraft_type = request.form.get('aircraft_type')
        departure_delay = request.form.get('departure_delay')
        aircraft_cleanliness = request.form.get('aircraft_cleanliness')
        friendliness = request.form.get('friendliness')
        entertainment_quality = request.form.get('entertainment_quality')
        food_quality = request.form.get('food_quality')
        user_friendliness = request.form.get('user_friendliness')

        new_review = Review(
            airline=airline,
            flight_number=flight_number,
            registration=registration,
            departure_airport=departure_airport,
            arrival_airport=arrival_airport,
            aircraft_type=aircraft_type,
            departure_delay=departure_delay,
            aircraft_cleanliness=aircraft_cleanliness,
            friendliness=friendliness,
            entertainment_quality=entertainment_quality,
            food_quality=food_quality,
            user_friendliness=user_friendliness
        )

        db.session.add(new_review)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_review.html')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template,request, redirect, url_for
from flask_migrate import Migrate
from models import db, Review
from sqlalchemy import or_, desc, func

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

@app.route('/review/<int:review_id>')
def view_review(review_id):
    review = Review.query.get_or_404(review_id)
    return render_template('review_detail.html', review=review)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # Ontvang de zoekparameters uit het formulier
        airline = request.form.get('airline')
        flight_number = request.form.get('flight_number')
        departure_airport = request.form.get('departure_airport')
        registration = request.form.get('registration')
        arrival_airport = request.form.get('arrival_airport')
        aircraft_type = request.form.get('aircraft_type')
        aircraft_cleanliness = request.form.get('aircraft_cleanliness')
        friendliness = request.form.get('friendliness')
        entertainment_quality = request.form.get('entertainment_quality')
        food_quality = request.form.get('food_quality')
        user_friendliness = request.form.get('user_friendliness')
        
        # Voer de zoekopdracht uit in de database (pas aan afhankelijk van je datamodel)
        reviews = Review.query.filter(
            Review.airline.ilike(f"%{airline}%"),
            Review.flight_number.ilike(f"%{flight_number}%"),
            Review.departure_airport.ilike(f"%{departure_airport}%"),
            Review.registration.ilike(f"%{registration}%"),
            Review.arrival_airport.ilike(f"%{arrival_airport}%"),
            Review.aircraft_type.ilike(f"%{aircraft_type}%"),
            Review.aircraft_cleanliness.ilike(f"%{aircraft_cleanliness}%"),
            Review.friendliness.ilike(f"%{friendliness}%"),
            Review.entertainment_quality.ilike(f"%{entertainment_quality}%"),
            Review.food_quality.ilike(f"%{food_quality}%"),
            Review.user_friendliness.ilike(f"%{user_friendliness}%"),
            # Voeg andere velden toe afhankelijk van je model
        ).all()

        # Geef de zoekresultaten door aan de template
        return render_template('search_results.html', reviews=reviews)

    # Als het geen POST-verzoek is, toon dan gewoon het zoekformulier
    return render_template('search.html')

@app.route('/top_airlines')
def top_airlines():
    # Haal de top airlines op basis van een bepaalde metriek (bijvoorbeeld vriendelijkheid)
    top_airlines = Review.query.order_by(desc(Review.friendliness)).limit(10).all()
    return render_template('top_airlines.html', top_airlines=top_airlines)

@app.route('/flop_airlines')
def flop_airlines():
    # Haal de flop airlines op basis van een bepaalde metriek (bijvoorbeeld vriendelijkheid)
    flop_airlines = Review.query.order_by(Review.friendliness).limit(10).all()
    return render_template('flop_airlines.html', flop_airlines=flop_airlines)

@app.route('/custom_ranking', methods=['GET', 'POST'])
def custom_ranking():
    if request.method == 'POST':
        # Ontvang de parameter van het formulier
        ranking_parameter = request.form.get('ranking_parameter')

        # Controleer of de parameter geldig is
        valid_parameters = ['friendliness', 'departure_delay', 'aircraft_cleanliness', 'entertainment_quality', 'food_quality', 'user_friendliness']  # Voeg hier alle geldige parameters toe

        if ranking_parameter in valid_parameters:
            # Gebruik de parameter voor het genereren van de lijsten
            top_list = Review.query.order_by(desc(getattr(Review, ranking_parameter))).limit(10).all()
            flop_list = Review.query.order_by(getattr(Review, ranking_parameter)).limit(10).all()

            return render_template('custom_ranking.html', top_list=top_list, flop_list=flop_list, parameter=ranking_parameter)
        else:
            return render_template('custom_ranking.html', error_message=f"Invalid parameter: {ranking_parameter}")

    # Als het geen POST-verzoek is, toon dan gewoon het formulier
    return render_template('ranking_form.html')

@app.route('/category_overviews')
def category_overviews():
    # Bereken de gemiddelde beoordelingen voor elke categorie
    average_ratings = {
        'Departure Delay': db.session.query(func.avg(Review.departure_delay)).scalar(),
        'Aircraft Cleanliness': db.session.query(func.avg(Review.aircraft_cleanliness)).scalar(),
        'Friendliness': db.session.query(func.avg(Review.friendliness)).scalar(),
        'Entertainment Quality': db.session.query(func.avg(Review.entertainment_quality)).scalar(),
        'Food Quality': db.session.query(func.avg(Review.food_quality)).scalar(),
        'User Friendliness': db.session.query(func.avg(Review.user_friendliness)).scalar(),
        # Voeg andere categorieën toe op basis van je datamodel
    }

    return render_template('category_overviews.html', average_ratings=average_ratings)

if __name__ == '__main__':
    app.run(debug=True)

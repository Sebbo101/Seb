from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from forms import RegistrationForm, LoginForm
from wtforms import StringField, PasswordField, SubmitField, validators
from models import db, Review, User
from sqlalchemy import or_, desc, func
from datetime import datetime

# Initialiseer de Flask-applicatie
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'  # SQLite-database bestand
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'geheime_sleutel'  # Geheime sleutel voor sessiebeheer
db.init_app(app)

# Initialiseer Flask-Migrate voor database migraties
migrate = Migrate(app, db)

# Initialiseer Flask-Login voor gebruikerssessies
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # De naam van de loginweergave

# Initialiseer Flask-Bcrypt voor wachtwoordhashing
bcrypt = Bcrypt(app)

# Functie om gebruikers te laden op basis van gebruikers-ID (nodig voor Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Startpunt van de applicatie - toont alle recensies
@app.route('/')
def index():
    reviews = Review.query.all()
    return render_template('index.html', reviews=reviews)

# Testroute voor de homepagina
@app.route('/home')
def home():
    reviews = Review.query.all()
    return render_template('home.html', reviews=reviews)

# Route voor gebruikersregistratie
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Ingevuld registratieformulier verwerken en gebruiker toevoegen aan database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)  # Render het register.html-bestand

# Route voor gebruikersinloggen
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Inloggen van de gebruiker en doorverwijzen naar de startpagina
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)  # Render het login.html-bestand

# Route voor uitloggen
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Route voor het overzicht van recensies
@app.route('/reviews')
def review_overview():
    reviews = Review.query.order_by(Review.timestamp.desc()).all()
    return render_template('review_overview.html', reviews=reviews)

# RESTful API voor recensies
@app.route('/api/reviews')
def api_reviews():
    filter_option = request.args.get('filter', 'all')

    # Haal recensies op basis van het filter
    if filter_option == 'all':
        reviews = Review.query.order_by(Review.timestamp.desc()).all()
    elif filter_option == 'airline':
        reviews = Review.query.order_by(Review.timestamp.desc()).all()
    # Voeg hier andere filters toe op basis van attributen (voeg extra elif-clausules toe)
    else:
        return jsonify([])

    # Maak een lijst met dictonaries van reviewgegevens
    reviews_data = [{'airline': review.airline, 'timestamp': review.timestamp} for review in reviews]

    return jsonify(reviews_data)

# Route voor het toevoegen van recensies
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

# Route voor het bekijken van individuele recensies
@app.route('/review/<int:review_id>')
def view_review(review_id):
    review = Review.query.get_or_404(review_id)
    return render_template('review_detail.html', review=review)

# Route voor het uitvoeren van zoekopdrachten
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

# Route voor het bekijken van de top-airlines
@app.route('/top_airlines')
def top_airlines():
    # Haal de top airlines op basis van een bepaalde metriek (bijvoorbeeld vriendelijkheid)
    top_airlines = Review.query.order_by(desc(Review.friendliness)).limit(10).all()
    return render_template('top_airlines.html', top_airlines=top_airlines)

# Route voor het bekijken van de flop-airlines
@app.route('/flop_airlines')
def flop_airlines():
    # Haal de flop airlines op basis van een bepaalde metriek (bijvoorbeeld vriendelijkheid)
    flop_airlines = Review.query.order_by(Review.friendliness).limit(10).all()
    return render_template('flop_airlines.html', flop_airlines=flop_airlines)

# Route voor het genereren van aangepaste ranglijsten
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

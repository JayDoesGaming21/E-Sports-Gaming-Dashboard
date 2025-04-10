from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime, timedelta

# Original code by: Dr. Corky Wicks
# Initialize Flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"

# Get the directory where the script is located
basedir = os.path.abspath(os.path.dirname(__file__))

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tournament_t_detail.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    address_line1 = db.Column(db.String(255), nullable=False)
    address_line2 = db.Column(db.String(255))
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.String(10), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Define Tournament model
class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    available = db.Column(db.Boolean, default=True)

# Define Tournament Detail model
class T_detail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    rental_date = db.Column(db.DateTime, default=datetime.utcnow)
    duration_days = db.Column(db.Integer, nullable=False)
    return_date = db.Column(db.DateTime, nullable=False)
    
    user = db.relationship('User', backref='T_detail')
    tournament = db.relationship('Tournament', backref='T_detail')

# Create database tables
with app.app_context():
    db.create_all()

# Route: Home (List Users, Tournaments, Tournament Details)
@app.route('/')
def index():
    Users = User.query.all()
    Tournaments = Tournament.query.all()
    T_details = T_detail.query.all()
    return render_template('index.html', Users=Users, Tournaments=Tournaments, T_details=T_details)

# Route: Add New User
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address1 = request.form['address_line1']
        address2 = request.form.get('address_line2', "")
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']
        mobile = request.form['mobile']
        email = request.form['email']
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists. Please use a different email.', 'danger')
            return redirect(url_for('add_user'))
        
        new_user = User(
            first_name=first_name, last_name=last_name, address_line1=address1,
            address_line2=address2, city=city, state=state, zipcode=zipcode,
            mobile=mobile, email=email
        )
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_user.html')

# Route: Add Tournament
@app.route('/add_tournament', methods=['GET', 'POST'])
def add_tournament():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', "")
        new_tournament = Tournament(name=name, description=description)
        db.session.add(new_tournament)
        db.session.commit()
        flash('Tournament added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_tournament.html')

# Route: Define Tournament
@app.route('/define_tournament', methods=['GET', 'POST'])
def define_tournament():
    users = User.query.all()
    available_tournament = Tournament.query.filter_by(available=True).all()
    
    if request.method == 'POST':
        user_id = request.form['user_id']
        tournament_id = request.form['tournament_id']
        duration_days = int(request.form['duration_days'])
        return_date = datetime.utcnow() + timedelta(days=duration_days)
        
        detail = T_detail(
            user_id=user_id, tournament_id=tournament_id,
            duration_days=duration_days, return_date=return_date
        )
        
        tournament = Tournament.query.get(tournament_id)
        tournament.available = False
        
        db.session.add(detail)
        db.session.commit()
        flash('Torunament defined successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('define_tournament.html', users=users, tournament=available_tournament)

# Route: Return Torunament
@app.route('/return_tournament/<int:t_detail_id>')
def return_tournament(t_detail_id):
    t_detail = T_detail.query.get_or_404(t_detail_id)
    tournament = Tournament.query.get(t_detail.tournament_id)
    tournament.available = True
    
    db.session.delete(t_detail)
    db.session.commit()
    flash('Tournament returned successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

[app.py]
@app.errorhandler(400)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
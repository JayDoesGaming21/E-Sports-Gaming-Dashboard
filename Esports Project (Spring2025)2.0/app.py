from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tournament.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define TournamentParticipant model
class TournamentParticipant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    game = db.Column(db.String(80), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        game = request.form['game']

        # Check if the username already exists
        existing_participant = TournamentParticipant.query.filter_by(name=name).first()
        if existing_participant:
            return redirect(url_for('profile_failure'))

        # Add new participant to the database
        new_participant = TournamentParticipant(name=name, email=email, game=game)
        db.session.add(new_participant)
        db.session.commit()

        return redirect(url_for('profile_success', name=name))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        participant = TournamentParticipant.query.filter_by(email=email).first()
        if participant:
            return redirect(url_for('profile_success', name=participant.name))
        return redirect(url_for('profile_failure'))
    
    return render_template('login.html')

@app.route('/profile_success')
def profile_success():
    name = request.args.get('name')
    return render_template('profile_success.html', name=name)

@app.route('/profile_failure')
def profile_failure():
    return render_template('profile_failure.html')

@app.route('/participant')
def participant():
    all_participant = TournamentParticipant.query.all()
    return render_template('participant.html', participants=all_participant)

@app.route('/success')
def success():
    name = request.args.get('name')
    return render_template('success.html', name=name)

@app.route('/failure')
def failure():
    return render_template('failure.html')

@app.route('/back')
def back():
    return render_template('back.html')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'tournaments.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Define Tournament model
class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(255), nullable=False)
    

# Create the database tables
with app.app_context():
    db.create_all()

# Route: Home (List Tournaments)
@app.route('/')
def tournament_index():
    tournaments = Tournament.query.all()
    return render_template('tournament_index.html', tournaments=tournaments)

# Route: Add New Tournament
@app.route('/add', methods=['GET', 'POST'])
def add_tournament():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        date = request.form['date']
       

        new_tournament = Tournament(
            name=name, location=location, date=date
        )
        db.session.add(new_tournament)
        db.session.commit()
        flash('Tournament added successfully!', 'success')
        return redirect(url_for('tournament_index'))
    
    return render_template('add_tournament.html')

# Route: Edit Tournament
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_tournament(id):
    tournament = Tournament.query.get_or_404(id)
    
    if request.method == 'POST':
        tournament.name = request.form['name']
        tournament.location = request.form['location']
        tournament.date = request.form['date']

        db.session.commit()
        flash('Tournament updated successfully!', 'success')
        return redirect(url_for('tournament_index'))
    
    return render_template('edit_tournament.html', tournament=tournament)

# Route: Delete Tournament
@app.route('/delete/<int:id>')
def delete_tournament(id):
    tournament = Tournament.query.get_or_404(id)
    db.session.delete(tournament)
    db.session.commit()
    flash('Tournament deleted successfully!', 'danger')
    return redirect(url_for('tournament_index'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

# Original code by: Dr. Corky Wicks
# Initialize Flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABSE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'admins.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Define Customer model
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

# Create the database tables
with app.app_context():
    db.create_all()

# Route: Home (List Users)
@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

# Route: Add New User
@app.route('/add', methods=['GET', 'POST'])
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

# Route: Edit User
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.address_line1 = request.form['address_line1']
        user.address_line2 = request.form.get('address_line2', "")
        user.city = request.form['city']
        user.state = request.form['state']
        user.zipcode = request.form['zipcode']
        user.mobile = request.form['mobile']
        user.email = request.form['email']

        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit_user.html', user=user)

# Route: Delete User
@app.route('/delete/<int:id>')
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

[app.py]
@app.errorhandler(400)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
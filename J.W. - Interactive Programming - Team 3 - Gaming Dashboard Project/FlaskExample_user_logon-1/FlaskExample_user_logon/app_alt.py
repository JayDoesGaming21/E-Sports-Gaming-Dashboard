from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Original code by: Dr. Corky Wicks
# Initialize Flask app
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Create database tables (run this before first use)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists. Try another one." # or: render_template('profile_failure.html', username=username)


        # Add new user to the database
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login')) # or 'profile_success'

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return render_template('success.html', username=username)
        else:
            return render_template('failure.html') # or: return render_template('failure.html',username=username)

    return render_template('login.html')

@app.route('/profile_success', methods=['GET'])
def profile_success():
    return render_template('profile_success.html')

@app.route('/update_profile', methods=['POST'])
def update_profile():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    if user:
        user.password = request.form['password']
        db.session.commit()
        return redirect(url_for('profile_success'))
    return "User not found."

if __name__ == '__main__':
    app.run(debug=True)
    
[app.py]
@app.errorhandler(400)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# ************************************************************************
# Python Application Prototype; Test App Code
# Author Name: Jaylon T. West
# Program Description: This is a test app code that I created to test out the Flask framework.
# The code is a simple user registration and login system using Flask and SQLite.
# The app allows users to register with a username and password, and then log in with those credentials.
# It also includes a profile success page that displays a success message after logging in.
# The app uses Flask-SQLAlchemy to interact with the SQLite database, and it includes error handling for duplicate usernames.
# The app is designed to be run in debug mode for development purposes.
# The database is created when the app is first run, and the tables are defined using SQLAlchemy models.
# The app includes routes for the index page, registration page, login page, and profile success page.
# The app uses HTML templates to render the pages, and it includes form handling for user input.
# The app is a simple example of how to use Flask and SQLite together to create a web application with user authentication.
# The app is designed to be easy to understand and modify, making it a good starting point for learning Flask and web development.
# ************************************************************************

"""
[LIST PROGRAM 1 CODE BELOW]

Numlist=[17,24,88,44,101,3.55,99,12]
Numlist.sort() # First sorted the numbers to make it easier for adding them
Sum=0
for x in Numlist:
    Sum+=x
print(Sum)

************************************************************************

[STRING PROGRAM CODE BELOW]

Phrase=str(input("Please enter a string: "))
# Using x as my character printer, it prints every character in the "Phrase" of the string.
for x in range(0,len(Phrase)):
    print(Phrase[x])
    
************************************************************************

[COMPLEX PROGRAM CODE BELOW]

# Hello there, and welcome to my program!

# Author Name: Jaylon T. West
# Program Description: Insurance Coverage

# To break this down in a synopsis, this program
# will determine what type of insurance coverage
# the user is qualified for depending on the information
# that user will input into the system.
# Here are my variables that I use for my program:

G=input("Sex?('M'or'F') ")
G=G.upper()
A=int(input("Age? "))
C=float(input("Cholesterol? "))

# Basically from here, I copied the blueprint/format
# of the Male information code and used it to format
# the female gender as well so they run the same code type
# with different information that the system is able to take
# from any user that puts any specific information for a particular
# type of insurance coverage.

if G=="M" and 20<=A<=40 and C<5.0:
    print("Preferred Plus")
elif G=="M" and 41<=A<=60 and C<6.5:
    print("Preferred")
elif G=="M" and A>60 and C<7.5:
    print("Standard")
#This is where I took the same code and did it for the female gender.
elif G=="F" and 20<=A<=45 and C<5.5:
    print("Preferred Plus")
elif G=="F" and 46<=A<=65 and C<7.0:
    print("Preferred")
elif G=="F" and A>65 and C<8.0:
    print("Standard")
else:#Anything else the user inputs besides the information given will receieve and error message from the system.
    print("Error")

************************************************************************

# The following code is for the error handling part of the whole project for input validation
# The error handling code is written in the app.py file

[ERROR HANDLING PROGRAM CODE BELOW]

Validinput=False # Input Checker

# Below is the loop that continues until the user puts in a valid number.

while Validinput!=True:
    Num=int(input("Enter a number:"))
    if 0<=Num<=10:
        Validinput=True
        print("Your input was valid.")
    else:
        print("Enter a number between 0 and 10")

# Hello there, and welcome to my program!

# Author Name: Jaylon T. West
# Program Description: Work and Power

# To break this down in a synopsis, this program
# will calculate the work(in Joules) and power
# (in Watts and in Horse Power) of an individual
# running up stairs. The user will enter in their
# mass(in kg), height/distance of the stairs(in m),
# and the time(in seconds) it took to go upstairs.
# (Below are some extra notes from class; an error checker for all variable types in the code.)
 
 def positive(x,vartype):
     while x<=0:
         try:
             print(vartype,"must be non-negative! Re-enter your",vartype)
             x=float(input())
         except ValueError:
             print("You typed in a string. This input must be between 0 and 100.")

     return x

 Validinput1=False
 Validinput2=False
 Validinput3=False
 Power=None
 Work=None
 Force=None
 HorsePower=None
 Acc=9.8
 while Validinput1!=True:
     try:
         M=float(input("What is your mass in Kg? "))
         M=positive(M,"Mass")
         if M>=0:
             Validinput1=True
             Force=M*Acc
         else:
             print("You typed in a Negative Number. The Number must be positive and greater than 0.")
            
     except ValueError:#Incase the user types something else other than a number.
         print("You have typed in a string. This input must be a positive number and greater than 0.")
        
 while Validinput2!=True:
     try:
         D=float(input("What is the height of the stairs in Meters? "))
         D=positive(D,"Distance")
         if D>=0:
             Validinput2=True
             Work=Force*D
         else:
             print("You entered a Negative number for height/distance. The Number must be positive and greater than 0.")
    
     except ValueError:#Incase the user types something else other than a number.
         print("You have typed in a string. This input must be a positive number and greater than 0.")
        
 while Validinput3!=True:
     try:
         T=float(input("How much Time did it take to go up the stairs in Seconds? "))
         T=positive(T,"Time")
         if T>=0:
             Validinput3=True
             Power=Work/T
             HorsePower=Power/746
         else:
             print("You entered an invalid time. Time must be greater than 0.")
            
     except ValueError:#Incase the user types something else other than a number.
         print("You have typed in a string. This input must be a positive number and greater than 0.")
        
     except ZeroDivisionError:#Incase the user types a number less than zero (like a negative number) for time, and time can't equal to or be lower than zero.
         print("Cannot be equal to 0.")

# (Below are all the templates I used to copy and paste into my code to start off with.)       

 except ZeroDivisionError:
         print("Cannot be equal to 0.")
        
 Force=M*Acc
 Work=Force*D
 Power=Work*T
 HorsePower=Power*HP

 print("Congratulations! You have typed in all valid inputs!")#The Result/Outcome after putting all three inputs in correctly.
 print("Your work done was: ",Work,"J")
 print("Your power was: ",Power,"Watts")
 print("Your horse power was: ",HorsePower,"HP")
"""
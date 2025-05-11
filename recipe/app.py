import re
from flask import Flask, jsonify, render_template, redirect, url_for, request, flash, session, send_from_directory

from .models.user import User  # Import the User model
import subprocess
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from datetime import datetime
import os
from dotenv import load_dotenv

from .models import db, User, Recipe  
from .models.recipes_data import default_recipes
from werkzeug.security import generate_password_hash, check_password_hash
import logging

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='static')
app.secret_key = "Krishna123"  # Secret key for session handling

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Load user by ID

# Database configuration
from .config import SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)
migrate = Migrate(app, db)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Routes
@app.route('/')
def index():
    return redirect(url_for('dashboard'))  # Redirect to the dashboard page

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/x-icon')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']  # Accept any password
        if len(password) < 8 or not re.search(r"[A-Z]", password) or not re.search(r"[!@#$%^&*]", password):
            flash("Password must be at least 8 characters long, include one uppercase letter, and one special symbol.", "error")
            return redirect(url_for('signup'))

        if password != request.form['confirm_password']:
            flash("Passwords do not match.", "error")
            return redirect(url_for('signup'))
        
        print(f"Received password: {password}")  # Debugging
  # Debugging

        user = User()  # Create a new User instance

        # Validate the input
        if not user.validate_name(name):
            flash("Name must contain only letters.")
            return redirect(url_for('signup'))
        
        if not user.validate_phone(phone):
            flash("Phone number must be exactly 10 digits.")
            return redirect(url_for('signup'))
        
        # Validate email format
        if "@" not in email or "." not in email.split("@")[-1]:
            flash("Invalid email format. Please include '@' and a domain.", "danger")
            return redirect(url_for('signup'))

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Please login.", "warning")
            return redirect(url_for('login'))

        # Create new user and hash the password
        new_user = User(
            name=name,
            dob=dob,
            phone=phone,
            email=email,
        )
        new_user.set_password(password)  # Hash the password
        flash("Signup successful! Please login.", "success")

        db.session.add(new_user)
        db.session.commit()
        
        flash("Signup successful! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        print(f"Login attempt - Email: {email}")  # Debug log
        
        user = User.query.filter_by(email=email).first()
        if user:
            print(f"User found with ID: {user.id}")  # Debug log
            if user.check_password(password):
                print("Password check passed")  # Debug log
                login_user(user)
                print(f"User authenticated: {current_user.is_authenticated}")  # Debug log
                flash("Login successful!", "success")
                next_page = request.args.get('next')
                return redirect(next_page or url_for('home'))
            else:
                print("Password check failed")  # Debug log
        else:
            print("User not found")  # Debug log
            
        flash("Invalid email or password.", "error")
        print("Login failed: Invalid email or password.")

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('dashboard'))  # Redirect directly to home

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if user:
            flash("Password reset instructions sent to your email.", "info")
        else:
            flash("Email not found.", "danger")

        return redirect(url_for('login'))

    return render_template('forgetpw.html')

@app.route('/home')
@login_required
def home():
    print(f"Home route - User authenticated: {current_user.is_authenticated}")  # Debug log
    if not current_user.is_authenticated:
        print("User not authenticated, redirecting to login")  # Debug log
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/recipe')
def recipe():
    recipe_content = request.args.get('recipe')  # Get the recipe from the query parameters
    return render_template('recipe.html', recipe=recipe_content)  # Pass the recipe to the template

@app.route('/biryani')
def biryani():
    return render_template('biryani.html')

@app.route('/chole_bhature')
def chole_bhature():
    return render_template('chole_bhature.html')

@app.route('/grilled_salmon')
def grilled_salmon():
    return render_template('grilled_salmon.html')

@app.route('/pasta')  # Fixed route name
def pasta_primavera():
    return render_template('pasta.html')

@app.route('/chocolate_cake')
def chocolate_cake():
    return render_template('chocolate_cake.html')

@app.route('/chilli_panner')
def chilli_panner():
    return render_template('chilli_panner.html')
@app.route('/maggi')
def maggi():
    return render_template('maggi.html')

@app.route('/fruit_salad')  # Fixed to match other routes
def fruit_salad():
    return render_template('fruit_salad.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/view_saved')
def view_saved():
    return render_template('view_saved.html')
 
@app.route('/history')
@login_required
def history():
    recipes = Recipe.query.all()
    return render_template('history.html', recipes=recipes)

@app.route('/submitrecipes')
def submitrecipes():
    return render_template('submitrecipes.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = current_user

    if request.method == 'POST':
        user.name = request.form['name']
        user.dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()
        user.email = request.form['email']
        user.phone = request.form['phone']

        # Update password if provided
        new_password = request.form.get('password')
        if new_password:
            user.password_hash = generate_password_hash(new_password)

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user)

@app.route('/notifications')
def notification():
    return render_template('notification.html')

@app.route('/contact_support')
def contact_support():
    return render_template('contact_support.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/get_recipe', methods=['GET'])
def get_recipe():
    recipe_name = request.args.get('name')
    logging.debug(f"Received request for recipe: {recipe_name}")  

    if recipe_name in default_recipes:
        return jsonify(default_recipes[recipe_name])  # Return JSON response
    else:
        return jsonify({"error": "Recipe not found"}), 404

@app.route('/fix_email')
def fix_email():
    user = User.query.filter_by(email='sky@gamil.com').first()
    if user:
        user.email = 'sky@gmail.com'
        db.session.commit()
        flash('Email fixed successfully!', 'success')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

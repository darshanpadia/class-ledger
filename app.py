# Core Flask modules
from flask import Flask, request, session, render_template, flash, url_for, redirect

# For password hashing and verification
from werkzeug.security import check_password_hash

# Flask-WTF for CSRF protection
from flask_wtf.csrf import CSRFProtect

# For environment variable management
import os
from dotenv import load_dotenv

# Import helper to get teacher from DB
from db import get_teacher_by_username

# Login and Logout forms using Flask-WTF
from forms import LoginForm, LogoutForm

# Load environment variables from .env file (e.g., SECRET_KEY)
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Secret key is used to secure session data and CSRF tokens
app.secret_key = os.environ.get('SECRET_KEY')

# Enable global CSRF protection for all forms and POST routes
csrf = CSRFProtect(app)


# -------------------------------------
# Route: /login
# Handles both GET (render login page) and POST (form submission)
# -------------------------------------
@app.route('/login', methods=['POST', 'GET'])
def teacher_login():
    form = LoginForm()  # Create form instance

    # If form was submitted and passed all validators
    if form.validate_on_submit():
        # Get data from form fields
        username = request.form['teacher_username']
        password = request.form['teacher_password']

        # Query DB to find teacher with given username
        teacher = get_teacher_by_username(username)

        # If teacher exists and password is correct
        if teacher and check_password_hash(teacher['password'], password):
            # Store teacher ID in session to track login
            session['teacher_id'] = teacher['id']
            return redirect(url_for('home'))  # Redirect to home/dashboard
        else:
            # Invalid login credentials
            flash("Invalid username or password.")  

    # For GET requests or failed POST, show the login page again
    return render_template('login.html', form=form)


# -------------------------------------
# Route: /logout
# Logs out the user (POST only) and clears session
# Protected with CSRF token via LogoutForm
# -------------------------------------
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clear all session data
    flash("You have been logged out.")
    return redirect(url_for('teacher_login'))  # Redirect back to login page


# -------------------------------------
# Route: /home
# Protected page that only logged-in users can access
# Uses LogoutForm for logout button CSRF safety
# -------------------------------------
@app.route('/home')
def home():
    # If not logged in, redirect to login
    if 'teacher_id' not in session:
        return redirect(url_for('teacher_login'))

    form = LogoutForm()  # CSRF-only form for secure logout button
    return render_template('home.html', form=form)


# -------------------------------------
# Run the Flask development server
# -------------------------------------
if __name__ == "__main__":
    app.run(debug=True)  # Set debug=True for development (not production)

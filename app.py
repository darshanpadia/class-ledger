# Core Flask modules
from flask import Flask, request, session, render_template, flash, url_for, redirect

# For password hashing and verification
from werkzeug.security import check_password_hash

# Flask-WTF for CSRF protection
from flask_wtf.csrf import CSRFProtect, generate_csrf

# For environment variable management
import os
from dotenv import load_dotenv

# Import helper to get teacher from DB, insert student record and get all student records
from db import (get_teacher_by_username, insert_student_record, get_all_student_records,
                delete_student_record, update_student_record, find_duplicate_record,
                  fetch_student_record_by_id, log_update_message_for_records)
# Login, Logout and Student forms using Flask-WTF
from forms import LoginForm, LogoutForm, StudentForm

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
        username = form.teacher_username.data
        password = form.teacher_password.data

        # Query DB to find teacher with given username
        teacher = get_teacher_by_username(username)

        # If teacher exists and password is correct
        if teacher and check_password_hash(teacher['password'], password):
            # Store teacher ID in session to track login
            session['teacher_id'] = teacher['id']
            return redirect(url_for('home'))  # Redirect to home/dashboard
        else:
            # Invalid login credentials
            flash("Invalid username or password.", "error")  

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
    flash("You have been logged out.", "info")
    return redirect(url_for('teacher_login'))  # Redirect back to login page


# -------------------------------------
# Route: /home
# Protected page that only logged-in users can access
# - Renders:
#     * List of all student records from the database
#     * CSRF-protected logout form
#     * CSRF-protected add-student form
# Uses LogoutForm for logout button CSRF safety
# -------------------------------------
@app.route('/home')
def home():
    # If not logged in, redirect to login
    if 'teacher_id' not in session:
        return redirect(url_for('teacher_login'))
    
    # Fetch all student records to display in the table
    student_records = get_all_student_records()

    # Create instances of forms for logout and adding a student
    logout_form = LogoutForm()   # CSRF-protected logout form
    student_form = StudentForm() # Add-student form with validation

    csrf_token = generate_csrf()

    # Render the home page with records and forms
    return render_template('home.html',
                           logout_form=logout_form,
                           student_form=student_form,
                           student_records=student_records,
                           csrf_token=csrf_token)


# ---------------------------------------------------------
# Route: /add_student
# - Handles POST request from student form submission
# - Validates input and inserts record into database if valid
# - Uses flash messages for success or validation errors
# ---------------------------------------------------------
@app.route('/add_student', methods=['POST'])
def add_student_record():
    form = StudentForm()

    # If all form fields are valid, insert the student record
    if form.validate_on_submit():
        student_name = form.student_name.data.strip()
        subject = form.subject.data.strip()
        marks = form.marks.data
        teacher_id = session.get('teacher_id')
        
        existing = find_duplicate_record(student_name, subject)  # Check for an existing record with same name & subject

        if existing:
            total_marks = int(existing['marks']) + int(marks)  # Add marks of existing and new
            if total_marks > 100:
                flash(f"Cannot add with existing record, total marks exceeding 100", "error")
                return redirect(url_for('home'))
            update_student_record(existing['id'], student_name, subject, total_marks)  # Update existing record
            flash(f"Merged with existing record. Total marks: {total_marks}", "success")  # Inform user of merge
        else:
            insert_student_record(student_name, subject, marks, teacher_id)  # Insert as new record if no duplicate
            flash("Student record successfully added.", "success")  # Confirmation message

    else:
        # If validation fails, flash each error message
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", "error")

    # Redirect back to the home page regardless of form result
    return redirect(url_for('home'))

# ---------------------------------------------------------
# Route: delete_student
# Handles POST request to delete a student record by ID
# Requires user to be logged in (session must contain teacher_id)
# Calls helper function to perform deletion from DB
# Shows success message and redirects to home page
# ---------------------------------------------------------
@app.route('/remove_record/<int:record_id>', methods=['POST'])
def remove_student_record(record_id):
    # Redirect to login if user is not authenticated
    if 'teacher_id' not in session:
        return redirect(url_for('teacher_login'))
    
    # Delete the student record from the database
    delete_student_record(record_id)
    
    # Show a confirmation message
    flash("Student record deleted.", "info")
    
    # Redirect to home page
    return redirect(url_for('home'))

# ---------------------------------------------------------
# Route: /edit_record/<record_id>
# Method: POST
# Description:
#   Handles inline editing of a student record.
#   - Validates that all input fields are non-empty.
#   - Ensures marks is a numeric value.
#   - Updates the record in the database if validation passes.
#   - Redirects back to the home page.
# ---------------------------------------------------------
@app.route('/edit_record/<int:record_id>', methods=['POST'])
def edit_student_record(record_id):
    # Get values from submitted form and remove surrounding whitespace

    record = fetch_student_record_by_id(record_id)

    name = request.form['name'].strip()
    subject = request.form['subject'].strip()
    marks = request.form['marks'].strip()  # ✅ FIX: call .strip()
    


    # Basic validation: all fields must be filled, marks must be a digit
    if not name or not subject or not marks.isdigit():
        flash("Invalid input", "error")  # Flash error message to UI
        return redirect(url_for('home'))  # Redirect back to home page
    
    existing = find_duplicate_record(name, subject)  # Check if a record with the same name and subject already exists

    # If the duplicate exists but it's not the same record being edited
    if existing and existing['id'] != record_id:
        flash("Duplicate record with same name and subject already exists", "error")  # Show error
        return redirect(url_for('home'))  # Redirect without updating

    # Convert marks to integer after validation
    marks = int(marks)

    # Call DB helper to update the student record
    if record['teacher_id'] == session.get('teacher_id'):
        update_student_record(record_id, name, subject, marks)
        msg = f'{record['teacher_id']} updated {name}'
        print(msg)
        print(log_update_message_for_records(msg))
    else :
        flash("Teacher dont have access to edit this entry.", "error")

    # Flash success message (optional)
    flash("Student record updated successfully.", "success")

    # Redirect back to the home/dashboard page
    return redirect(url_for('home'))

@app.route('/')
def index():
    return redirect(url_for('home'))
   
# -------------------------------------
# Run the Flask development server
# -------------------------------------
if __name__ == "__main__":
    app.run(debug=True)  # Set debug=True for development (not production)

# Import base form class from Flask-WTF
from flask_wtf import FlaskForm

# Import field types from WTForms
from wtforms import StringField, PasswordField, SubmitField, IntegerField

# Import validators to enforce field requirements
from wtforms.validators import DataRequired, NumberRange, Length, Regexp

# ---------------------------------------------
# LoginForm: Used to handle teacher login input
# Includes CSRF protection automatically via FlaskForm
# ---------------------------------------------
class LoginForm(FlaskForm):
    # Input field for the teacher's username (required)
    teacher_username = StringField('Username', validators=[DataRequired()])

    # Input field for the teacher's password (required)
    teacher_password = PasswordField('Password', validators=[DataRequired()])

    # Submit button labeled "Login"
    submit = SubmitField('Login')

# ---------------------------------------------
# LogoutForm: Minimal form used only for CSRF-protected logout
# Even though there's no user input, CSRF token is included for safety
# ---------------------------------------------
class LogoutForm(FlaskForm):
    # Submit button labeled "Logout"
    submit = SubmitField('Logout')

# ---------------------------------------------------------
# StudentForm: Form used to add a new student record
# - Fields: student_name, subject, marks
# - Includes validation to ensure:
#     * Name is at least 2 characters and contains only letters/spaces
#     * Subject is required
#     * Marks must be a number between 1 and 100
# - CSRF token is automatically included for security
# ---------------------------------------------------------
class StudentForm(FlaskForm):
    # Student name field - must be at least 2 characters long and only contain letters and spaces
    student_name = StringField(
        'Name',
        validators=[
            DataRequired(),  # Ensures the field is not left empty
            Length(min=2),   # Requires at least 2 characters
            Regexp(r'^[A-Za-z\s]+$', message="Name must contain only letters")  # Enforces letters and spaces only
        ]
    )

    # Subject field - required text input
    subject = StringField(
        'Subject',
        validators=[DataRequired()]  # Ensures the field is not left empty
    )

    # Marks field - must be an integer between 1 and 100
    marks = IntegerField(
        'Marks',
        validators=[
            DataRequired(),  # Ensures the field is not left empty
            NumberRange(min=1, max=100, message="Marks must be a positive number between 1-100")  # Validates range
        ]
    )

    # Submit button for the form
    submit = SubmitField("Add Student")

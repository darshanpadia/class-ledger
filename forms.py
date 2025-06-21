# Import base form class from Flask-WTF
from flask_wtf import FlaskForm

# Import field types from WTForms
from wtforms import StringField, PasswordField, SubmitField, IntegerField

# Import validators to enforce field requirements
from wtforms.validators import DataRequired

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


class StudentForm(FlaskForm):
    student_name = StringField('Nmae', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    marks = IntegerField('Marks', validators=[DataRequired()])
    submit = SubmitField("Add Student")
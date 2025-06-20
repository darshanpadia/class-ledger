from flask import Flask, request, session, render_template, flash, url_for, redirect
from werkzeug.security import check_password_hash
import os
from dotenv import load_dotenv
from db import get_teacher_by_username
from flask_wtf.csrf import CSRFProtect
from forms import LoginForm, LogoutForm

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
csrf = CSRFProtect(app)

@app.route('/login', methods=['POST', 'GET'])
def teacher_login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['teacher_username']
        password = request.form['teacher_password']

        teacher = get_teacher_by_username(username)

        if teacher and check_password_hash(teacher['password'], password):
            session['teacher_id'] = teacher['id']
            return redirect(url_for('home'))
        else:
            flash("Invalid username or psasword.")  

    return render_template('login.html', form=form)


@app.route('/logout', methods=['POST'])
def logout():
    session.clear
    flash("You have been logged out.")
    return redirect(url_for('teacher_login'))


@app.route('/home')
def home():
    if 'teacher_id' not in session:
        return redirect(url_for('teacher_login'))
    form = LogoutForm()
    return render_template('home.html', form=form)


if __name__ == "__main__":
    app.run(debug="True")
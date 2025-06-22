🧑‍🏫 Class-Ledger – Flask App
```A secure and scalable Flask-based dashboard application that allows teachers to add, edit, delete, and manage student records with validations and user-friendly UI. The app uses Flask-WTF forms, CSRF protection, password hashing, and a clean architecture ready for production and future enhancements.



📌 Features
```Secure teacher login with hashed password

Dashboard to:

Add student records

Edit or delete records inline

Prevent duplicate student–subject entries

Merge marks if same student–subject pair is added again

Form validations and CSRF protection on all actions

Flash messages for all user actions



Tests:

✅ Unit tests

✅ Integration tests

✅ End-to-end flow

Clean folder structure and scalable 



🛠️ Tech Stack
```Flask – Web framework

Flask-WTF – Form handling with CSRF protection

Werkzeug – Password hashing

SQLite – Lightweight relational database

Python-Dotenv – Manage secrets

Pytest – Testing framework

HTML + CSS (Minimal) – UI 



🚀 Getting Started
```Follow these steps to run the project locally:

1️⃣ Clone or Download
git clone https://github.com/darshanpadia/class-ledger.git
Or download and extract the project zip manually.
cd class-ledger-main

2️⃣ Set Up Python Environment
Create and activate a virtual environment:
python -m venv venv
venv\Scripts\Activate.ps1   # For Windows PowerShell
# OR
source venv/bin/activate    # For macOS/

3️⃣ Install Dependencies
pip install -r requirements.

4️⃣ Create .env File
In the root directory (next to app.py, db.py, models.py, etc.), create a .env file manually or rename the existing .env-sample:
mv .env-sample .env  # macOS/Linux
ren .env-sample .env  # Windows
Then add the following variables:
TEACHER_USERNAME=teacher1
TEACHER_PASSWORD=pass123
SECRET_KEY=ca894f6cf62f65a5ee7d9cee42483628e0b651d3c7f5e3a0c4b6a1d59f6d0236
You may change these values as per your preference.

5️⃣ Initialize the Database
Run the following once to create tables:
python models.py
This script creates necessary tables if they don’t exist.

6️⃣ Run the Server
Use this to start the Flask app:
python app.py
⚠️ flask run won't work here due to the file named db.py, which may conflict with system modules.



✅ Application Flow
```🔐 Login
Navigate to http://127.0.0.1:5000/login

Use credentials from your .env file

Example:

Username: teacher1

Password: pass123



🧾 Dashboard Features
```Once logged in, you will be redirected to the dashboard (/home) where you can:

Add Student Record

Provide Name, Subject, and Marks

If the student–subject pair already exists, marks will be added to the existing record

Edit Student Record

Click “Edit”, update fields, then “Update”

Cannot change to duplicate student–subject pair

Delete Student

Click “Delete” to remove the record

Flash Messages

Appear for all actions (e.g., “Record added”, “Invalid input”, etc.)



🧪 Testing
```Run the test suite using:
pytest
Tests include:

Type	Coverage
Unit Tests	DB operations (insert, find, update, delete)
Integration	Login → Add → Merge
End-to-End	Login → Home → Logout → Home



🛡️ Security Best Practices 

```CSRF protection on all forms

Passwords stored as secure hashes

Parameterized queries to prevent SQL injection

Input validation on frontend and backend

Session-based authentication



## 🧩 Folder Structure

```text
teacher-portal/
├── app.py              # Main Flask app
├── models.py           # DB table creation
├── db.py               # DB connection & queries
├── forms.py            # Flask-WTF form classes
├── .env                # Environment variables
├── requirements.txt    # Python dependencies
│
├── templates/          # HTML templates (login, home)
├── static/             # CSS / JS
└── tests/              # All test cases
    ├── test_db.py
    ├── test_auth.py
    └── test_student_records.py
🧠 Why This Architecture?
This project is designed for:

Readability – Clean separation of concerns

Security – Adheres to Flask security best practices

Testability – Full coverage from DB to frontend

Scalability – Easy to add features like multiple users, charts, or export features in the future



📬 Feedback or Contributions?
Feel free to fork, open issues, or contribute enhancements. All improvements and suggestions are welcome!
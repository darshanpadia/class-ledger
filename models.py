import sqlite3  # SQLite module to interact with the database
import os       # For accessing environment variables
from dotenv import load_dotenv  # To load variables from a .env file
from werkzeug.security import generate_password_hash  # To securely hash passwords

# Load environment variables from .env file
load_dotenv()

# ---------------------------------------------
# Function: create_tables
# - Creates required tables if they don't exist
# - Inserts default teacher with hashed password
# ---------------------------------------------
def create_tables():
    # Get teacher credentials from environment variables
    teacher_username = os.environ.get('TEACHER_USERNAME')
    teacher_password = os.environ.get('TEACHER_PASSWORD')

    # Connect to SQLite database (creates file if it doesn't exist)
    conn = sqlite3.connect('class-ledger.db')
    cur = conn.cursor()

    # Create 'teachers' table if it doesn't already exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,  -- Username must be unique and not null
            password TEXT NOT NULL          -- Password will be stored as a hash
        )
    ''')

    # Create 'student_records' table if it doesn't already exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS student_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            subject TEXT NOT NULL,
            marks INT NOT NULL
        )
    ''')

    # Add unique index on student_name + subject (case-insensitive)
    cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS unique_student_subject
        ON student_records (LOWER(student_name), LOWER(subject));
    """)


    # Hash the teacher's password securely using Werkzeug
    hashed_password = generate_password_hash(teacher_password)

    # Insert default teacher into the teachers table
    # 'INSERT OR IGNORE' ensures it won't add duplicate if username already exists
    cur.execute(
        'INSERT OR IGNORE INTO teachers (username, password) VALUES (?, ?)',
        (teacher_username, hashed_password)
    )

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# ---------------------------------------------
# Run create_tables() when this script is run directly
# ---------------------------------------------
if __name__ == '__main__':
    create_tables()

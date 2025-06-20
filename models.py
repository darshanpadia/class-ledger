import sqlite3 
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

def create_tables():
    teacher_username = os.environ.get('TEACHER_USERNAME')
    teacher_password = os.environ.get('TEACHER_PASSWORD')
    conn = sqlite3.connect('class-ledger.db')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NON NULL UNIQUE,
            password TEXT NON NULL
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS student_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NON NULL,
            subject TEXT NON NULL,
            marks INT NON NULL
        )
    ''')
    hashed_password = generate_password_hash(teacher_password)
    cur.execute('INSERT OR IGNORE INTO teachers (username, password) VALUES (?, ?)', (teacher_username, hashed_password))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
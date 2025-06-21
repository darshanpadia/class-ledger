import sqlite3  # SQLite module to interact with the database

# ---------------------------------------------
# Function: get_db_connection
# Establishes and returns a connection to the SQLite database
# Enables row access by column name (dictionary-like)
# ---------------------------------------------
def get_db_connection():
    # Connect to the SQLite database (creates file if it doesn't exist)
    conn = sqlite3.connect("class-ledger.db")

    # Configure connection to return rows as dictionary-like objects
    conn.row_factory = sqlite3.Row

    return conn

# ---------------------------------------------
# Function: get_teacher_by_username
# Fetches a teacher record from the DB by username
# Used during login to validate credentials
# ---------------------------------------------
def get_teacher_by_username(username):
    conn = get_db_connection()     # Get database connection
    cur = conn.cursor()            # Create a cursor to execute queries

    # Use parameterized query to prevent SQL injection
    cur.execute("SELECT * FROM teachers WHERE username = ?", (username,))

    # Fetch one matching record (since username is unique)
    teacher = cur.fetchone()

    # Close the database connection
    conn.close()

    return teacher  # Returns None if no match found

def insert_student_record(student_name, subject, marks):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO student_records (student_name,subject,marks) VALUES (?, ?, ?)", (student_name, subject, marks))
    conn.commit()
    conn.close()

def get_all_student_records():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM student_records')
    students = cur.fetchall()
    conn.close()
    return students


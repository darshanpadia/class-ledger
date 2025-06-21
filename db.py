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

# ---------------------------------------------------------
# insert_student_record:
# Inserts a new student record into the student_records table
# - Parameters:
#     * student_name (str): Name of the student
#     * subject (str): Subject for which the marks are recorded
#     * marks (int): Marks obtained by the student
# - Establishes DB connection, executes INSERT query, commits and closes
# ---------------------------------------------------------
def insert_student_record(student_name, subject, marks):
    conn = get_db_connection()  # Establish database connection
    cur = conn.cursor()         # Create a cursor object for executing SQL statements

    # Execute an INSERT SQL statement to add the student data
    cur.execute(
        "INSERT INTO student_records (student_name, subject, marks) VALUES (?, ?, ?)",
        (student_name, subject, marks)
    )

    conn.commit()  # Commit the transaction to save changes
    conn.close()   # Close the database connection


# ---------------------------------------------------------
# get_all_student_records:
# Retrieves all student records from the student_records table
# - Returns:
#     * List of sqlite3.Row objects representing student records
# - Establishes DB connection, executes SELECT query, fetches all rows
# ---------------------------------------------------------
def get_all_student_records():
    conn = get_db_connection()  # Establish database connection
    cur = conn.cursor()         # Create a cursor object

    # Execute a SELECT SQL statement to fetch all records
    cur.execute('SELECT * FROM student_records')
    students = cur.fetchall()   # Retrieve all rows from the query result

    conn.close()                # Close the database connection
    return students             # Return the list of student records

# ---------------------------------------------------------
# Function: delete_student_record
# Deletes a student record from the database based on the ID
# Parameter: record_id (int) - ID of the student to delete
# ---------------------------------------------------------
def delete_student_record(record_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM student_records WHERE id=?", (record_id,))
    conn.commit()
    conn.close()

# ---------------------------------------------------------
# Function: update_student_record
# Updates an existing student record in the database
#
# Parameters:
#   - student_id (int): ID of the student to update
#   - name (str): New name for the student
#   - subject (str): New subject name
#   - marks (int): New marks value
#
# Steps:
#   1. Prepare an UPDATE SQL query using parameterized values
#   2. Execute the query to update the student record by ID   
# ---------------------------------------------------------
def update_student_record(student_id, name, subject, marks):
    conn = get_db_connection()
    cur = conn.cursor()    

    cur.execute("""
        UPDATE student_records 
        SET student_name = ?, subject = ?, marks = ? 
        WHERE id = ?
    """, (name, subject, marks, student_id))

    conn.commit()  
    conn.close()    

# ---------------------------------------------------------
# Function: find_duplicate_record
# Checks for an existing student record with the same
# name and subject (case-insensitive) in the database.
# Parameters:
#   - student_name (str): Name of the student to search.
#   - subject (str): Subject associated with the student.
# Returns:
#   - Matching record (sqlite3.Row) if found, else None
# ---------------------------------------------------------
def find_duplicate_record(student_name, subject):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM student_records
        WHERE LOWER(student_name) = LOWER(?) AND LOWER(subject) = LOWER(?)
    """, (student_name, subject))
    row = cur.fetchone()
    conn.close()
    return row

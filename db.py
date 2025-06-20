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

import sqlite3

def get_db_connection():
    conn = sqlite3.connect("class-ledger.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_teacher_by_username(username):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM teachers WHERE username = ?", (username,))
    teacher = cur.fetchone()
    conn.close()
    return teacher
 
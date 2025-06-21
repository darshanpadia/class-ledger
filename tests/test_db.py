import unittest
import sqlite3
import sys
import os

# Add the project root directory to sys.path so you can import from db.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import db
from db import (
    get_db_connection, get_teacher_by_username, insert_student_record,
    get_all_student_records, delete_student_record,
    update_student_record, find_duplicate_record
)


class DBConnectionTests(unittest.TestCase):
    def test_get_db_connection_returns_row_factory(self):
        conn = get_db_connection()
        self.assertIsNotNone(conn)
        self.assertEqual(conn.row_factory, sqlite3.Row)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cur.fetchall()
        self.assertIsInstance(tables, list)
        conn.close()


class TeacherDBTests(unittest.TestCase):
    def test_get_teacher_by_username(self):
        teacher = get_teacher_by_username("teacher1")
        self.assertIsNotNone(teacher)
        self.assertIn('username', teacher.keys())


class StudentDBTests(unittest.TestCase):
    def setUp(self):
        # Create an in-memory SQLite DB and patch the connection
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

        # Create student_records table
        self.cur.execute('''
            CREATE TABLE student_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                subject TEXT NOT NULL,
                marks INT NOT NULL
            )
        ''')
        self.conn.commit()

        # Patch get_db_connection to return this in-memory DB
        self.original_get_db_connection = db.get_db_connection
        db.get_db_connection = lambda: self.conn

    def tearDown(self):
        db.get_db_connection = self.original_get_db_connection
        self.conn.close()

    def test_insert_and_fetch(self):
        insert_student_record("Alice", "Math", 90, conn=self.conn)
        records = get_all_student_records(conn=self.conn)
        self.assertEqual(len(records), 1)


    def test_find_duplicate(self):
        insert_student_record("Alice", "Math", 90)
        result = find_duplicate_record("alice", "math")
        self.assertIsNotNone(result)
        self.assertEqual(result["marks"], 90)

    def test_update_record(self):
        insert_student_record("Bob", "Science", 80)
        record = find_duplicate_record("Bob", "Science")
        update_student_record(record["id"], "Bob", "Science", 95)
        updated = find_duplicate_record("Bob", "Science")
        self.assertEqual(updated["marks"], 95)

    def test_delete_record(self):
        insert_student_record("Charlie", "History", 70)
        record = find_duplicate_record("Charlie", "History")
        delete_student_record(record["id"])
        self.assertIsNone(find_duplicate_record("Charlie", "History"))

class StudentDBTests(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self.cur.execute('''
            CREATE TABLE student_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                subject TEXT NOT NULL,
                marks INT NOT NULL
            )
        ''')
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_insert_and_fetch(self):
        insert_student_record("Alice", "Math", 90, conn=self.conn)
        records = get_all_student_records(conn=self.conn)
        assert len(records) == 1
        assert records[0]["student_name"] == "Alice"

    def test_find_duplicate(self):
        insert_student_record("Alice", "Math", 90, conn=self.conn)
        result = find_duplicate_record("alice", "math", conn=self.conn)
        assert result is not None
        assert result["marks"] == 90

    def test_update_record(self):
        insert_student_record("Bob", "Science", 80, conn=self.conn)
        record = find_duplicate_record("Bob", "Science", conn=self.conn)
        update_student_record(record["id"], "Bob", "Science", 95, conn=self.conn)
        updated = find_duplicate_record("Bob", "Science", conn=self.conn)
        assert updated["marks"] == 95

    def test_delete_record(self):
        insert_student_record("Charlie", "History", 70, conn=self.conn)
        record = find_duplicate_record("Charlie", "History", conn=self.conn)
        delete_student_record(record["id"], conn=self.conn)
        result = find_duplicate_record("Charlie", "History", conn=self.conn)
        assert result is None

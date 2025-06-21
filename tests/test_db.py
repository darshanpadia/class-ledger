import unittest
from db import get_teacher_by_username, get_db_connection
import sqlite3
import sys
import os

# Add the project root directory to sys.path so you can import from app root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class DBConnectionTests(unittest.TestCase):
    def test_get_db_connection_returns_row_factory(self):
        """Test DB connection and ensure row_factory is set correctly."""
        conn = get_db_connection()
        self.assertIsNotNone(conn)
        self.assertEqual(conn.row_factory, sqlite3.Row)

        # Try a harmless query to confirm connection
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cur.fetchall()
        self.assertIsInstance(tables, list)
        conn.close()

class TestDB(unittest.TestCase):
    def test_get_teacher_by_username(self):
        """Test fetching a known teacher from the DB."""
        teacher = get_teacher_by_username("teacher1") 
        self.assertIsNotNone(teacher)
        self.assertIn('username', teacher.keys())

import unittest
from app import app
from flask import session
import sys
import os
import re

# Add the project root directory to sys.path so you can import from app root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class AuthTests(unittest.TestCase):
    @staticmethod
    def extract_csrf_token(html):
        """Extract CSRF token from hidden input field in HTML."""
        match = re.search(r'name="csrf_token" type="hidden" value="([^"]+)"', html)
        return match.group(1) if match else None

    def setUp(self):
        """Configure the test client before each test."""
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_login_page_loads(self):
        """Test if login page loads with all necessary fields."""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
        self.assertIn(b'name="teacher_username"', response.data)
        self.assertIn(b'name="teacher_password"', response.data)
        self.assertIn(b'name="csrf_token"', response.data)

    def test_valid_login(self):
        """Test login flow with valid credentials."""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        csrf_token = self.extract_csrf_token(response.get_data(as_text=True))
        self.assertIsNotNone(csrf_token)

        response = self.client.post('/login', data={
            'teacher_username': os.getenv("TEACHER_USERNAME"),
            'teacher_password': os.getenv("TEACHER_PASSWORD"),
            'csrf_token': csrf_token
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logout', response.data)

    def test_invalid_login(self):
        """Test login with invalid credentials displays error."""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        csrf_token = self.extract_csrf_token(response.get_data(as_text=True))
        self.assertIsNotNone(csrf_token)

        response = self.client.post('/login', data={
            'teacher_username': "wronguser",
            'teacher_password': "wrongpass",
            'csrf_token': csrf_token
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password.', response.data)

    def test_logout_clears_session(self):
        """Test if logout clears session and redirects to login."""
        with self.client as c:
            login_page = c.get('/login')
            csrf_token_login = self.extract_csrf_token(login_page.get_data(as_text=True))
            self.assertIsNotNone(csrf_token_login)

            login_response = c.post('/login', data={
                'teacher_username': os.getenv("TEACHER_USERNAME"),
                'teacher_password': os.getenv("TEACHER_PASSWORD"),
                'csrf_token': csrf_token_login
            }, follow_redirects=True)
            self.assertEqual(login_response.status_code, 200)
            self.assertIn(b'Logout', login_response.data)

            home_page = c.get('/home')
            csrf_token_logout = self.extract_csrf_token(home_page.get_data(as_text=True))
            self.assertIsNotNone(csrf_token_logout)

            logout_response = c.post('/logout', data={
                'csrf_token': csrf_token_logout
            }, follow_redirects=True)
            self.assertEqual(logout_response.status_code, 200)
            self.assertIn(b'You have been logged out.', logout_response.data)
            self.assertIn(b'Login', logout_response.data)

    def test_login_home_logout_flow(self):
        """End-to-end test: login → home → logout → protected page access."""
        with self.client as c:
            login_page = c.get('/login')
            csrf_login = self.extract_csrf_token(login_page.get_data(as_text=True))
            self.assertIsNotNone(csrf_login)

            login_response = c.post('/login', data={
                'teacher_username': os.getenv("TEACHER_USERNAME"),
                'teacher_password': os.getenv("TEACHER_PASSWORD"),
                'csrf_token': csrf_login
            }, follow_redirects=True)
            self.assertEqual(login_response.status_code, 200)
            self.assertIn(b'Logout', login_response.data)

            home_response = c.get('/home')
            self.assertEqual(home_response.status_code, 200)
            self.assertIn(b'Logout', home_response.data)

            csrf_logout = self.extract_csrf_token(home_response.get_data(as_text=True))
            self.assertIsNotNone(csrf_logout)

            logout_response = c.post('/logout', data={
                'csrf_token': csrf_logout
            }, follow_redirects=True)
            self.assertEqual(logout_response.status_code, 200)
            self.assertIn(b'You have been logged out.', logout_response.data)

            home_after_logout = c.get('/home', follow_redirects=True)
            self.assertEqual(home_after_logout.status_code, 200)
            self.assertIn(b'Login', home_after_logout.data)

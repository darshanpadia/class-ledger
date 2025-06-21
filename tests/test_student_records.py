import unittest
import os
import re
from app import app

class StudentRecordTests(unittest.TestCase):

    @staticmethod
    def extract_csrf_token(html):
        match = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', html)
        return match.group(1) if match else None

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_add_student_and_merge(self):
        with self.client as c:
            # Login
            login_page = c.get('/login')
            csrf_login = self.extract_csrf_token(login_page.get_data(as_text=True))
            c.post('/login', data={
                'teacher_username': os.getenv("TEACHER_USERNAME"),
                'teacher_password': os.getenv("TEACHER_PASSWORD"),
                'csrf_token': csrf_login
            }, follow_redirects=True)

            # First add
            home_page = c.get('/home')
            csrf_add = self.extract_csrf_token(home_page.get_data(as_text=True))
            c.post('/add_student', data={
                'student_name': 'John Doe',
                'subject': 'Math',
                'marks': 50,
                'csrf_token': csrf_add
            }, follow_redirects=True)

            # Add again to trigger merge
            home_page2 = c.get('/home')
            csrf_add_2 = self.extract_csrf_token(home_page2.get_data(as_text=True))
            response = c.post('/add_student', data={
                'student_name': 'John Doe',
                'subject': 'Math',
                'marks': 50,
                'csrf_token': csrf_add_2
            }, follow_redirects=True)

            self.assertIn(b'Merged with existing record', response.data)

    def test_edit_and_delete_student(self):
        with self.client as c:
            # Login
            login_page = c.get('/login')
            csrf_login = self.extract_csrf_token(login_page.get_data(as_text=True))
            c.post('/login', data={
                'teacher_username': os.getenv("TEACHER_USERNAME"),
                'teacher_password': os.getenv("TEACHER_PASSWORD"),
                'csrf_token': csrf_login
            }, follow_redirects=True)

            # Add a student
            home = c.get('/home')
            csrf_token = self.extract_csrf_token(home.get_data(as_text=True))
            c.post('/add_student', data={
                'student_name': 'Jane',
                'subject': 'Biology',
                'marks': 40,
                'csrf_token': csrf_token
            }, follow_redirects=True)

            # Get the record ID of newly added student
            response = c.get('/home')
            match = re.search(r'<tr id="row-(\d+)">.*?Jane.*?Biology', response.get_data(as_text=True), re.DOTALL)
            record_id = match.group(1)

            # Edit student
            c.post(f'/edit_record/{record_id}', data={
                'name': 'Jane Updated',
                'subject': 'Biology',
                'marks': 75,
                'csrf_token': csrf_token
            }, follow_redirects=True)

            updated_page = c.get('/home')
            self.assertIn(b'Jane Updated', updated_page.data)
            self.assertIn(b'75', updated_page.data)

            # Delete student
            c.post(f'/remove_record/{record_id}', data={
                'csrf_token': csrf_token
            }, follow_redirects=True)
            final_page = c.get('/home')
            self.assertNotIn(b'Jane Updated', final_page.data)


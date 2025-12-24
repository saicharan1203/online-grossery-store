import unittest
from app import create_app
from extensions import db
from models import User
import re

class ResetPasswordTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_reset_password_flow(self):
        try:
            # 1. Register with email
            response = self.client.post('/register', data=dict(
                username='testuser',
                email='test@example.com',
                password='oldpassword'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            
            # Logout
            self.client.get('/logout', follow_redirects=True)
            
            # 2. Request Reset
            response = self.client.post('/forgot_password', data=dict(
                email='test@example.com'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            
            # Extract token from flash message (simulated email)
            # In real app, we'd check email. Here we check the flash message or DB.
            with self.app.app_context():
                user = User.query.filter_by(email='test@example.com').first()
                self.assertIsNotNone(user.reset_token)
                token = user.reset_token
                
            # 3. Reset Password
            response = self.client.post(f'/reset_password/{token}', data=dict(
                password='newpassword'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Password reset successfully', response.data)
            
            # 4. Login with new password
            response = self.client.post('/login', data=dict(
                username='testuser',
                password='newpassword'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Logout', response.data)
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise e

if __name__ == '__main__':
    unittest.main()

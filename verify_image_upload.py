import unittest
import os
from io import BytesIO
from app import create_app
from extensions import db
from models import User, Product

class ImageUploadTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # Create admin user
            admin = User(username='admin', password_hash='hash', is_admin=True)
            db.session.add(admin)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_image_upload(self):
        # Login as admin
        with self.client.session_transaction() as sess:
            sess['_user_id'] = '1'

        # Create a dummy image
        data = {
            'name': 'Test Product',
            'category': 'Test Category',
            'price': 10.0,
            'stock': 5,
            'image': (BytesIO(b'fake image data'), 'test_image.png')
        }

        response = self.client.post('/admin/add_product', data=data, content_type='multipart/form-data', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            product = Product.query.filter_by(name='Test Product').first()
            self.assertIsNotNone(product)
            self.assertEqual(product.image_url, 'images/test_image.png')
            
            # Verify file exists (mocking save would be better but for integration test we check file system)
            # Since we are running in a real env, we should check if file was created in static/images
            # However, in this test environment, we might want to clean it up.
            image_path = os.path.join('static', 'images', 'test_image.png')
            self.assertTrue(os.path.exists(image_path))
            
            # Cleanup
            if os.path.exists(image_path):
                os.remove(image_path)

if __name__ == '__main__':
    unittest.main()

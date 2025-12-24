import unittest
from app import create_app
from extensions import db
from models import User, Product, CartItem

class AddToCartTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Create user
            user = User(username='shopper', password_hash='hash')
            db.session.add(user)
            
            # Create product
            product = Product(name='Test Product', category='Test', price=10.0, stock=10)
            db.session.add(product)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_to_cart_ajax(self):
        # Login
        with self.client.session_transaction() as sess:
            sess['_user_id'] = '1'
            
        # Add to cart via AJAX
        response = self.client.get('/add_to_cart/1', headers={'X-Requested-With': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['cart_count'], 1)
        self.assertEqual(data['cart_total'], 10.0)
        
        # Verify DB
        with self.app.app_context():
            item = CartItem.query.first()
            self.assertIsNotNone(item)
            self.assertEqual(item.quantity, 1)

if __name__ == '__main__':
    unittest.main()

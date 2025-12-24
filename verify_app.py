import os
import unittest
from app import create_app
from extensions import db
from models import User, Product, CartItem, Order

class GroceryAppTestCase(unittest.TestCase):
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
            
    def test_register_and_login(self):
        # Register
        response = self.client.post('/register', data=dict(
            username='testuser',
            password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logout', response.data)
        
        # Logout
        self.client.get('/logout', follow_redirects=True)
        
        # Login
        response = self.client.post('/login', data=dict(
            username='testuser',
            password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logout', response.data)

    def test_admin_add_product(self):
        # Create admin
        with self.app.app_context():
            admin = User(username='admin', password_hash='hash', is_admin=True)
            db.session.add(admin)
            db.session.commit()
            
        # Login as admin
        with self.client.session_transaction() as sess:
            sess['_user_id'] = '1'
            
        # Add product
        response = self.client.post('/admin/add_product', data=dict(
            name='Apple',
            category='Fruit',
            price=1.5,
            stock=100
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        with self.app.app_context():
            product = Product.query.first()
            self.assertEqual(product.name, 'Apple')
            self.assertEqual(product.price, 1.5)

    def test_cart_and_checkout(self):
        # Setup: User and Product
        with self.app.app_context():
            user = User(username='shopper', password_hash='hash')
            product = Product(name='Banana', category='Fruit', price=0.5, stock=10)
            db.session.add(user)
            db.session.add(product)
            db.session.commit()
            
        # Login
        with self.client.session_transaction() as sess:
            sess['_user_id'] = '1'
            
        # Add to cart
        self.client.get('/add_to_cart/1', follow_redirects=True)
        
        with self.app.app_context():
            cart_item = CartItem.query.first()
            self.assertEqual(cart_item.quantity, 1)
            
        # Checkout
        response = self.client.get('/checkout', follow_redirects=True)
        self.assertIn(b'Order placed successfully', response.data)
        
        with self.app.app_context():
            order = Order.query.first()
            self.assertIsNotNone(order)
            self.assertEqual(order.total_price, 0.5)

if __name__ == '__main__':
    unittest.main()

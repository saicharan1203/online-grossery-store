from app import create_app
from extensions import db
from models import User, Product

app = create_app()

with app.app_context():
    print("Creating tables...")
    db.create_all()
    print("Tables created.")
    
    # Seed if empty
    if not User.query.filter_by(username='admin').first():
        print("Seeding database...")
        # We can call the seed logic directly or just let the user hit /seed
        # But let's do it here to be sure
        from werkzeug.security import generate_password_hash
        
        admin = User(
            username='admin', 
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'), 
            is_admin=True
        )
        db.session.add(admin)
        
        if not Product.query.first():
            products = [
                Product(name='Apple', category='Fruit', price=1.20, stock=100, image_url='images/apple.png'),
                Product(name='Banana', category='Fruit', price=0.50, stock=150, image_url='images/fruit.png'),
                Product(name='Milk', category='Dairy', price=3.50, stock=50, image_url='images/dairy.png'),
                Product(name='Bread', category='Bakery', price=2.00, stock=40, image_url='images/bakery.png'),
                Product(name='Eggs', category='Dairy', price=4.00, stock=60, image_url='images/dairy.png'),
                Product(name='Chicken Breast', category='Meat', price=7.50, stock=30, image_url='images/vegetable.png'),
                Product(name='Rice', category='Grains', price=5.00, stock=80, image_url='images/bakery.png'),
                Product(name='Tomato', category='Vegetable', price=0.80, stock=120, image_url='images/vegetable.png')
            ]
            db.session.bulk_save_objects(products)
            
        db.session.commit()
        print("Database seeded.")
    else:
        print("Database already seeded.")

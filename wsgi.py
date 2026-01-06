from app import create_app
from extensions import db
from models import Product, User
from product_catalog import PRODUCTS as CATALOG_PRODUCTS
from werkzeug.security import generate_password_hash

app = create_app()

# Auto-seed database on startup if empty
with app.app_context():
    db.create_all()
    
    # Create admin if doesn't exist
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
    
    # Seed products if database is empty
    if not Product.query.first():
        for p in CATALOG_PRODUCTS:
            product = Product(
                name=p.name,
                category=p.category,
                price=p.price,
                stock=100,
                image_url=p.image_url,
                description=f"Fresh {p.name.lower()} - high quality {p.category.lower()} product"
            )
            db.session.add(product)
        db.session.commit()
        print(f"Database seeded with {len(CATALOG_PRODUCTS)} products")

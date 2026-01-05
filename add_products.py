from dataclasses import asdict

from app import create_app
from extensions import db
from models import Product
from product_catalog import PRODUCTS

app = create_app()

products_to_add = [asdict(product) for product in PRODUCTS]

with app.app_context():
    print(f"Adding {len(products_to_add)} products...")
    added_count = 0
    for item in products_to_add:
        # Check if product already exists
        existing_product = Product.query.filter_by(name=item['name']).first()
        if not existing_product:
            new_product = Product(
                name=item['name'],
                category=item['category'],
                price=item['price'],
                image_url=item['image_url'],
                stock=100  # Default stock
            )
            db.session.add(new_product)
            added_count += 1
        else:
            # Update existing product to match user request
            existing_product.category = item['category']
            existing_product.price = item['price']
            existing_product.image_url = item['image_url']
            print(f"Updated existing product: {item['name']}")
    
    db.session.commit()
    print(f"Successfully added {added_count} new products.")

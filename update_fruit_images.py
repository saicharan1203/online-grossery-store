from app import create_app
from extensions import db
from models import Product

app = create_app()

IMAGE_MAP = {
    'Banana': 'images/banana.png',
    'Mango': 'images/mango.png',
    'Coconut': 'images/coconut.png',
    'Strawberry': 'images/strawberry.png',
    'Watermelon Slice': 'images/watermelon.png',
    # Pineapple failed, so we skip it or leave it as fruit.png
}

with app.app_context():
    for name, image_path in IMAGE_MAP.items():
        product = Product.query.filter_by(name=name).first()
        if product:
            product.image_url = image_path
            print(f"Updated {name} to {image_path}")
        else:
            print(f"Product {name} not found!")
            
    db.session.commit()
    print("Database updated.")

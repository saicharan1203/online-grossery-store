from app import create_app
from models import Product

app = create_app()

with app.app_context():
    products = Product.query.order_by(Product.category, Product.name).all()
    print(f"{'ID':<5} {'Name':<20} {'Category':<15} {'Image URL'}")
    print("-" * 60)
    for p in products:
        print(f"{p.id:<5} {p.name:<20} {p.category:<15} {p.image_url}")

from app import create_app
from models import Product

app = create_app()

with app.app_context():
    count = Product.query.count()
    print(f"Total products in database: {count}")
    
    # List all products by category
    products = Product.query.order_by(Product.category, Product.name).all()
    current_category = None
    for p in products:
        if p.category != current_category:
            print(f"\n--- {p.category} ---")
            current_category = p.category
        print(f"{p.name} - ${p.price:.2f}")

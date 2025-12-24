from app import create_app
from extensions import db
from models import Product

app = create_app()

with app.app_context():
    # Find products pointing to images/logo.png
    products = Product.query.filter_by(image_url='images/logo.png').all()
    
    print(f"Found {len(products)} products with broken logo path.")
    
    for p in products:
        p.image_url = 'logo.png' # Point to static/logo.png
        print(f"Updated {p.name} to use 'logo.png'")
        
    if products:
        db.session.commit()
        print("Database updated.")
    else:
        print("No changes needed.")

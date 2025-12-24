from app import create_app
from extensions import db
from models import Product

app = create_app()

# Products to update with correct image paths
updates = {
    'Shampoo Bottle': 'images/home_shampoo.png',
    'Body Soap': 'images/home_soap.png',
    'Laundry Detergent': 'images/home_detergent.png',
    'Toothpaste Tube': 'images/home_toothpaste.png'
}

with app.app_context():
    print("Updating product images...")
    for product_name, image_path in updates.items():
        product = Product.query.filter_by(name=product_name).first()
        if product:
            old_image = product.image_url
            product.image_url = image_path
            print(f"✓ {product_name}: {old_image} → {image_path}")
        else:
            print(f"✗ Product not found: {product_name}")
    
    db.session.commit()
    print("\n✅ Database updated successfully!")
    
    # Verify updates
    print("\nVerifying updates:")
    for product_name in updates.keys():
        product = Product.query.filter_by(name=product_name).first()
        if product:
            print(f"  {product_name}: {product.image_url}")

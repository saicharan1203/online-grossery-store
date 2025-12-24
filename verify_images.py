import os
from app import create_app
from models import Product

app = create_app()

with app.app_context():
    products = Product.query.all()
    static_folder = os.path.join(app.root_path, 'static')
    
    missing_count = 0
    print("Checking product images...")
    for p in products:
        image_path = os.path.join(static_folder, p.image_url.replace('/', os.sep))
        if not os.path.exists(image_path):
            print(f"[MISSING] {p.name}: {p.image_url}")
            missing_count += 1
        # else:
        #     print(f"[OK] {p.name}: {p.image_url}")
            
    if missing_count == 0:
        print("\nAll products have valid images!")
    else:
        print(f"\nFound {missing_count} missing images.")

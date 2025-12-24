import os
from app import create_app
from extensions import db
from models import Product

app = create_app()

# Map categories to existing placeholder images
# Based on file listing: apple.png, bakery.png, dairy.png, fruit.png, vegetable.png
CATEGORY_IMAGES = {
    'Fruit': 'images/fruit.png',
    'Dairy': 'images/dairy.png',
    'Bakery': 'images/bakery.png',
    'Meat': 'images/meat.png', # Assuming this might not exist, need to check or map to default
    'Grains': 'images/grains.png', # Likely doesn't exist
    'Vegetable': 'images/vegetable.png',
    'Snacks': 'images/snacks.png',
    'Pantry': 'images/pantry.png',
    'Beverage': 'images/beverage.png',
    'Household': 'images/household.png'
}

# Fallback for categories without a specific image
DEFAULT_IMAGE = 'images/logo.png' 

def fix_images():
    with app.app_context():
        products = Product.query.all()
        updated_count = 0
        
        static_folder = os.path.join(app.root_path, 'static')
        
        for product in products:
            # Check if current image exists
            image_path = os.path.join(static_folder, product.image_url.replace('/', os.sep))
            
            if not os.path.exists(image_path):
                print(f"Missing image for {product.name}: {product.image_url}")
                
                # Determine new image
                category = product.category
                new_image = CATEGORY_IMAGES.get(category)
                
                # Check if the category image exists, otherwise use a safe default or keep checking
                if new_image:
                    cat_image_path = os.path.join(static_folder, new_image.replace('/', os.sep))
                    if not os.path.exists(cat_image_path):
                         # If category image also doesn't exist, try to find *any* valid image or use a known one
                         # For now, let's map unknown categories to a known one like 'fruit.png' or just leave it if we can't find better
                         # Actually, let's check what we have.
                         # We know we have: apple.png, bakery.png, dairy.png, fruit.png, vegetable.png
                         if category == 'Meat': new_image = 'images/dairy.png' # Temporary fallback
                         elif category == 'Grains': new_image = 'images/bakery.png'
                         elif category == 'Snacks': new_image = 'images/bakery.png'
                         elif category == 'Pantry': new_image = 'images/vegetable.png'
                         elif category == 'Beverage': new_image = 'images/fruit.png'
                         elif category == 'Household': new_image = 'images/logo.png'
                         else: new_image = 'images/logo.png'
                else:
                    new_image = 'images/logo.png'

                print(f"  -> Updating to {new_image}")
                product.image_url = new_image
                updated_count += 1
        
        if updated_count > 0:
            db.session.commit()
            print(f"Updated {updated_count} products with missing images.")
        else:
            print("No missing images found (or logic failed).")

if __name__ == '__main__':
    fix_images()

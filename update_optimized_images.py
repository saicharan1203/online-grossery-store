"""Script to update product images in the database after optimization."""

from app import create_app
from extensions import db
from models import Product
import os

IMAGE_DIR = "static/images"

def get_available_images():
    """Get all available image files in the images directory."""
    images = {}
    for filename in os.listdir(IMAGE_DIR):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.webp')):
            # Store without extension for matching
            base_name = os.path.splitext(filename)[0].lower()
            images[base_name] = f"images/{filename}"
    return images

def update_product_images():
    app = create_app()
    with app.app_context():
        available_images = get_available_images()
        products = Product.query.all()
        
        updated_count = 0
        
        for product in products:
            current_image = product.image_url
            if not current_image:
                continue
            
            # Check if current image exists
            current_path = os.path.join("static", current_image)
            if os.path.exists(current_path):
                continue  # Image exists, no update needed
            
            # Try to find a matching WebP version
            base_name = os.path.splitext(os.path.basename(current_image))[0].lower()
            
            # Check for WebP version
            if base_name in available_images:
                new_image = available_images[base_name]
                product.image_url = new_image
                print(f"Updated '{product.name}': {current_image} -> {new_image}")
                updated_count += 1
        
        db.session.commit()
        print(f"\n✅ Updated {updated_count} product images in database!")

if __name__ == "__main__":
    update_product_images()

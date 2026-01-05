"""Script to update product images in the database with newly uploaded images."""

from app import create_app
from extensions import db
from models import Product

# Mapping of product names to their new image URLs
IMAGE_UPDATES = {
    # Previously updated
    "Aged Cheese": "images/aged cheese.webp",
    "Cabbage": "images/cabbage.webp",
    "Butter Cookies": "images/butter cookies.webp",
    "Bread": "images/bread.webp",
    # New uploads
    "Butter Croissant": "images/butter croissant.webp",
    "Butter Slab": "images/butter slab.webp",
    "Carrot Bunch": "images/carrot bunch.webp",
    "Chicken Breast": "images/chicken breast.webp",
    "Chili Powder": "images/chilly powder.webp",
    "Chocolate Muffin": "images/chocolate muffin.webp",
    "Fresh Milk": "images/fresh milk.webp",
    "Garlic Bulb": "images/garlic bulb.webp",
    "Greek Yogurt": "images/greek yogurt.webp",
    "Herbal Tea": "images/herbal tea.webp",
    "Honey Jar": "images/honey jar.webp",
}

def update_product_images():
    app = create_app()
    with app.app_context():
        updated_count = 0
        not_found = []
        
        for product_name, new_image_url in IMAGE_UPDATES.items():
            product = Product.query.filter_by(name=product_name).first()
            if product:
                old_url = product.image_url
                product.image_url = new_image_url
                print(f"Updated '{product_name}': {old_url} -> {new_image_url}")
                updated_count += 1
            else:
                not_found.append(product_name)
        
        db.session.commit()
        print(f"\n✅ Updated {updated_count} product images successfully!")
        
        if not_found:
            print(f"\n⚠️ Products not found in database: {not_found}")

if __name__ == "__main__":
    update_product_images()

from pathlib import Path

from app import create_app
from extensions import db
from models import Product
from product_catalog import (
    CATEGORY_FALLBACKS,
    PRODUCT_CATEGORY_MAP,
    PRODUCT_IMAGE_MAP,
)

app = create_app()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
DEFAULT_PLACEHOLDER = CATEGORY_FALLBACKS.get("Fruit", "images/fruit.png")
category_fallbacks = CATEGORY_FALLBACKS


def asset_exists(rel_path: str) -> bool:
    return (STATIC_DIR / rel_path).exists()


product_images = PRODUCT_IMAGE_MAP.copy()

with app.app_context():
    print("=" * 60)
    print("UPDATING ALL PRODUCT IMAGES")
    print("=" * 60)
    
    updated_count = 0
    not_found_count = 0
    already_correct = 0
    fallback_count = 0
    
    for product_name, correct_image in product_images.items():
        product = Product.query.filter_by(name=product_name).first()
        if product:
            target_image = correct_image
            if not asset_exists(correct_image):
                category = PRODUCT_CATEGORY_MAP.get(product_name) or product.category
                fallback = category_fallbacks.get(category, DEFAULT_PLACEHOLDER)
                target_image = fallback
                fallback_count += 1
                print(f"⚠ {product_name:25} asset missing, falling back to {fallback}")

            if product.image_url != target_image:
                old_image = product.image_url
                product.image_url = target_image
                print(f"✓ {product_name:25} {old_image:30} → {target_image}")
                updated_count += 1
            else:
                already_correct += 1
        else:
            print(f"✗ NOT FOUND: {product_name}")
            not_found_count += 1
    
    db.session.commit()
    
    print("=" * 60)
    print(f"✅ Updated: {updated_count} products")
    print(f"✓  Already correct: {already_correct} products")
    if fallback_count:
        print(f"⚠  Used fallbacks for {fallback_count} products (asset missing)")
    if not_found_count > 0:
        print(f"⚠  Not found: {not_found_count} products")
    print("=" * 60)
    print("\n🎉 Database update complete!")

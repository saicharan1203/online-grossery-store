"""Script to identify and clean up unused/duplicate images."""

import os
from app import create_app
from models import Product
from product_catalog import PRODUCTS, CATEGORY_FALLBACKS, ADDITIONAL_IMAGE_OVERRIDES

IMAGE_DIR = "static/images"

# System images that should NOT be deleted
SYSTEM_IMAGES = {
    "upi_qr.webp",  # Payment QR code
}

def get_used_images():
    """Get all images that are actually used by products."""
    used_images = set()
    
    # From product catalog
    for product in PRODUCTS:
        image_path = product.image_url.replace("images/", "")
        used_images.add(image_path)
    
    # From category fallbacks
    for category, image_path in CATEGORY_FALLBACKS.items():
        image_path = image_path.replace("images/", "")
        used_images.add(image_path)
    
    # From additional overrides
    for name, (category, image_path) in ADDITIONAL_IMAGE_OVERRIDES.items():
        image_path = image_path.replace("images/", "")
        used_images.add(image_path)
    
    # From database
    app = create_app()
    with app.app_context():
        products = Product.query.all()
        for product in products:
            if product.image_url:
                image_path = product.image_url.replace("images/", "")
                used_images.add(image_path)
    
    return used_images

def get_all_images():
    """Get all images in the images folder."""
    all_images = set()
    for filename in os.listdir(IMAGE_DIR):
        if os.path.isfile(os.path.join(IMAGE_DIR, filename)):
            all_images.add(filename)
    return all_images

def analyze_images():
    """Analyze which images are used and which are unused."""
    used_images = get_used_images()
    all_images = get_all_images()
    
    # Find unused images (excluding system images)
    unused_images = all_images - used_images - SYSTEM_IMAGES
    
    # Find missing images (referenced but don't exist)
    missing_images = used_images - all_images
    
    return used_images, unused_images, missing_images

def cleanup_unused_images(dry_run=True):
    """Remove unused images."""
    used_images, unused_images, missing_images = analyze_images()
    
    print("=" * 60)
    print("IMAGE CLEANUP REPORT")
    print("=" * 60)
    
    print("\nSummary:")
    print("   Total images in folder: {}".format(len(get_all_images())))
    print("   Images actually used: {}".format(len(used_images)))
    print("   System images (kept): {}".format(len(SYSTEM_IMAGES)))
    print("   Unused images to delete: {}".format(len(unused_images)))
    
    if missing_images:
        print("\n[!] Missing images (referenced but not found):")
        for img in sorted(missing_images):
            print("   - {}".format(img))
    
    if unused_images:
        print("\n[DELETE] Unused images to be deleted:")
        total_size = 0
        for img in sorted(unused_images):
            filepath = os.path.join(IMAGE_DIR, img)
            size = os.path.getsize(filepath) / 1024  # KB
            total_size += size
            print("   - {} ({:.1f} KB)".format(img, size))
        
        print("\n   Total space to be freed: {:.1f} KB ({:.2f} MB)".format(total_size, total_size/1024))
        
        if not dry_run:
            print("\nDeleting unused images...")
            deleted_count = 0
            for img in unused_images:
                filepath = os.path.join(IMAGE_DIR, img)
                try:
                    os.remove(filepath)
                    print("   [OK] Deleted: {}".format(img))
                    deleted_count += 1
                except Exception as e:
                    print("   [ERROR] Error deleting {}: {}".format(img, e))
            
            print("\n[DONE] Deleted {} unused images!".format(deleted_count))
        else:
            print("\n[DRY RUN] No files were deleted.")
            print("   Run with --delete flag to actually delete files.")
    else:
        print("\n[OK] No unused images found!")
    
    return unused_images

if __name__ == "__main__":
    import sys
    
    # Check if --delete flag is passed
    if len(sys.argv) > 1 and sys.argv[1] == "--delete":
        cleanup_unused_images(dry_run=False)
    else:
        print("Running in DRY RUN mode (no files will be deleted)")
        print("To actually delete files, run: python cleanup_images.py --delete\n")
        cleanup_unused_images(dry_run=True)

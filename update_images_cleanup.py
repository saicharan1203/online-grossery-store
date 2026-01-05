"""
Script to update products with new images and delete old unused images.
"""
from app import create_app
from extensions import db
from models import Product
import os

# New images mapping - using the new webp images you added
NEW_IMAGE_MAPPING = {
    # Fruits
    "Apple": "images/apple.webp",
    "Banana": "images/banana.webp",
    "Mango": "images/mango.webp",
    "Pineapple": "images/pineapple.webp",
    "Coconut": "images/coconut.webp",
    "Strawberry": "images/strawberry.webp",
    "Watermelon Slice": "images/watermelon.webp",
    
    # Dairy
    "Fresh Milk": "images/fresh milk.webp",
    "Greek Yogurt": "images/greek yogurt.webp",
    "Butter Slab": "images/butter slab.webp",
    "Aged Cheese": "images/aged cheese.webp",
    "Paneer Cubes": "images/panner cubes.webp",
    "Curds Cup": "images/curds cup.webp",
    "Farm Eggs": "images/farm eggs.webp",
    
    # Bakery
    "Sourdough Bread": "images/bread.webp",
    "Butter Croissant": "images/butter croissant.webp",
    "Chocolate Muffin": "images/chocolate muffin.webp",
    "Cinnamon Roll": "images/cinnamon rolls.webp",
    "Wholegrain Bagel": "images/wholegrain bagel.webp",
    "Vanilla Cupcake": "images/vanilla cupcake.webp",
    
    # Meat & Seafood
    "Chicken Breast": "images/chicken breast.webp",
    "Fish Fillet": "images/fish fillet.webp",
    "Mutton Cuts": "images/mutton cuts.webp",
    "Salmon Steak": "images/salmon steak.webp",
    "Shrimp Basket": "images/shrimp basket.webp",
    "Turkey Bacon": "images/turkey bacon.webp",
    
    # Grains
    "Basmati Rice": "images/basmati rice.webp",
    "Whole Wheat Pasta": "images/whole wheat pasta.webp",
    "Quinoa Pack": "images/quinoa pack.webp",
    "Rolled Oats": "images/rolled oats.webp",
    "Wheat Grains": "images/wheat grains.webp",
    "Cornmeal": "images/corn meal.webp",
    
    # Vegetables
    "Lettuce Head": "images/lettuce head.webp",
    "Cabbage": "images/cabbage.webp",
    "Carrot Bunch": "images/carrot bunch.webp",
    "Onion Bag": "images/onion bag.webp",
    "Garlic Bulb": "images/garlic bulb.webp",
    "Green Peas": "images/green peas.webp",
    "Sweet Corn": "images/sweet corn.webp",
    "Tomato": "images/tomato.webp",
    
    # Snacks
    "Potato Chips": "images/potato chis.webp",
    "Chocolate Bar": "images/chocolate bar.webp",
    "Butter Cookies": "images/butter cookies.webp",
    "Trail Mix": "images/trail mix.webp",
    "Ice Cream Tub": "images/ice cream tub.webp",
    "Pretzel Bites": "images/pretzel bites.webp",
    
    # Pantry
    "Honey Jar": "images/honey jar.webp",
    "Jam Spread": "images/jam spread.webp",
    "Peanut Butter": "images/peanut butter.webp",
    "All-Purpose Flour": "images/all purpose flour.webp",
    "Lentils Mix": "images/lentils mix.webp",
    "Kidney Beans": "images/kidney beans.webp",
    "Turmeric Powder": "images/turmeric powder.webp",
    "Chili Powder": "images/chilly powder.webp",
    
    # Beverages
    "Coffee Beans": "images/coffee beans.webp",
    "Herbal Tea": "images/herbal tea.webp",
    "Juice Box": "images/juice box.webp",
    "Soft Drink Can": "images/soft drink can.webp",
    "Sparkling Soda": "images/sparkling soda.webp",
    "Energy Drink": "images/energy drinks.webp",
    
    # Household
    "Shampoo Bottle": "images/home_shampoo.webp",
    "Body Soap": "images/home_soap.webp",
    "Laundry Detergent": "images/home_detergent.webp",
    "Toothpaste Tube": "images/home_toothpaste.webp",
    "Paper Towels": "images/home_paper.webp",
    "Dish Soap": "images/home_dishsoap.webp",
}

# Old PNG images to delete (keeping only webp versions)
OLD_IMAGES_TO_DELETE = [
    "bakery_bagel.png",
    "bakery_cupcake.png",
    "bakery_sourdough.png",
    "bev_juice.png",
    "bev_soda.png",
    "bev_softdrink.png",
    "dairy_eggs.png",
    "dairy_paneer.png",
    "grains_oats.png",
    "grains_pasta.png",
    "grains_quinoa.png",
    "grains_rice.png",
    "grains_wheat.png",
    "meat_fish.png",
    "meat_mutton.png",
    "meat_salmon.png",
    "meat_shrimp.png",
    "meat_turkey.png",
    "pantry_beans.png",
    "pantry_flour.png",
    "pantry_jam.png",
    "pantry_lentils.png",
    "pantry_peanut.png",
    "pantry_turmeric.png",
    "pineapple.png",
    "snack_chips.png",
    "snack_chocolate.png",
    "snack_icecream.png",
    "snack_pretzel.png",
    "snack_trailmix.png",
    "veg_corn.png",
    "veg_lettuce.png",
    "veg_onion.png",
    "veg_peas.png",
    "veg_tomato.png",
]


def update_products_and_cleanup():
    """Update product images and delete old unused images"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("UPDATING PRODUCT IMAGES & CLEANING UP OLD FILES")
        print("=" * 60)
        
        # Update product images in database
        print("\n📦 Updating product images in database...")
        updated_count = 0
        
        for product_name, new_image in NEW_IMAGE_MAPPING.items():
            product = Product.query.filter_by(name=product_name).first()
            if product:
                old_image = product.image_url
                product.image_url = new_image
                updated_count += 1
                print(f"   ✓ {product_name}: {old_image} → {new_image}")
        
        db.session.commit()
        print(f"\n✅ Updated {updated_count} product images")
        
        # Delete old PNG images
        print("\n🗑️  Deleting old unused images...")
        images_dir = os.path.join(os.path.dirname(__file__), 'static', 'images')
        deleted_count = 0
        deleted_size = 0
        
        for old_image in OLD_IMAGES_TO_DELETE:
            image_path = os.path.join(images_dir, old_image)
            if os.path.exists(image_path):
                file_size = os.path.getsize(image_path)
                os.remove(image_path)
                deleted_count += 1
                deleted_size += file_size
                print(f"   ✓ Deleted: {old_image} ({file_size / 1024:.1f} KB)")
            else:
                print(f"   - Not found: {old_image}")
        
        print(f"\n✅ Deleted {deleted_count} old images")
        print(f"💾 Freed up {deleted_size / 1024:.1f} KB of space")
        
        # Count remaining images
        remaining_images = [f for f in os.listdir(images_dir) if f.endswith(('.webp', '.png', '.jpg'))]
        print(f"\n📊 Remaining images: {len(remaining_images)}")
        
        print("\n" + "=" * 60)
        print("IMAGE UPDATE COMPLETE!")
        print("=" * 60)


if __name__ == "__main__":
    update_products_and_cleanup()

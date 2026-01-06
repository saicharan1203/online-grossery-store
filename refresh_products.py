"""
Script to refresh all products in the database.
Deletes existing products and adds new ones from the product catalog.
"""
from app import create_app
from extensions import db
from models import Product, CartItem, OrderItem, Wishlist, Review
import os

# Product data with updated images (using webp where available)
FRESH_PRODUCTS = [
    # Fruits
    {"name": "Apple", "category": "Fruit", "price": 1.20, "stock": 100, "image_url": "images/apple.webp", 
     "description": "Fresh red apples, crisp and sweet"},
    {"name": "Banana", "category": "Fruit", "price": 0.55, "stock": 150, "image_url": "images/banana.webp",
     "description": "Ripe yellow bananas, perfect for snacking"},
    {"name": "Mango", "category": "Fruit", "price": 1.80, "stock": 80, "image_url": "images/mango.webp",
     "description": "Sweet and juicy tropical mangoes"},
    {"name": "Pineapple", "category": "Fruit", "price": 2.40, "stock": 60, "image_url": "images/pineapple.webp",
     "description": "Fresh tropical pineapple"},
    {"name": "Coconut", "category": "Fruit", "price": 2.10, "stock": 70, "image_url": "images/coconut.webp",
     "description": "Fresh whole coconut"},
    {"name": "Strawberry", "category": "Fruit", "price": 2.90, "stock": 90, "image_url": "images/strawberry.webp",
     "description": "Fresh sweet strawberries"},
    {"name": "Watermelon Slice", "category": "Fruit", "price": 4.60, "stock": 40, "image_url": "images/watermelon.webp",
     "description": "Refreshing watermelon slices"},
    
    # Dairy
    {"name": "Fresh Milk", "category": "Dairy", "price": 3.40, "stock": 120, "image_url": "images/fresh milk.webp",
     "description": "Farm-fresh whole milk"},
    {"name": "Greek Yogurt", "category": "Dairy", "price": 2.10, "stock": 100, "image_url": "images/greek yogurt.webp",
     "description": "Creamy Greek-style yogurt"},
    {"name": "Butter Slab", "category": "Dairy", "price": 2.60, "stock": 80, "image_url": "images/butter slab.webp",
     "description": "Premium quality butter"},
    {"name": "Aged Cheese", "category": "Dairy", "price": 4.80, "stock": 50, "image_url": "images/aged cheese.webp",
     "description": "Mature aged cheese"},
    {"name": "Paneer Cubes", "category": "Dairy", "price": 3.70, "stock": 70, "image_url": "images/panner cubes.webp",
     "description": "Fresh cottage cheese cubes"},
    {"name": "Curds Cup", "category": "Dairy", "price": 1.90, "stock": 90, "image_url": "images/curds cup.webp",
     "description": "Fresh natural yogurt"},
    {"name": "Farm Eggs", "category": "Dairy", "price": 4.00, "stock": 100, "image_url": "images/farm eggs.webp",
     "description": "Free-range farm eggs (dozen)"},
    
    # Bakery
    {"name": "Sourdough Bread", "category": "Bakery", "price": 3.30, "stock": 60, "image_url": "images/bread.webp",
     "description": "Artisan sourdough loaf"},
    {"name": "Butter Croissant", "category": "Bakery", "price": 1.70, "stock": 80, "image_url": "images/butter croissant.webp",
     "description": "Flaky butter croissant"},
    {"name": "Chocolate Muffin", "category": "Bakery", "price": 2.20, "stock": 70, "image_url": "images/chocolate muffin.webp",
     "description": "Rich chocolate chip muffin"},
    {"name": "Cinnamon Roll", "category": "Bakery", "price": 2.80, "stock": 50, "image_url": "images/cinnamon rolls.webp",
     "description": "Warm cinnamon swirl roll"},
    {"name": "Wholegrain Bagel", "category": "Bakery", "price": 1.40, "stock": 90, "image_url": "images/wholegrain bagel.webp",
     "description": "Healthy wholegrain bagel"},
    {"name": "Vanilla Cupcake", "category": "Bakery", "price": 2.60, "stock": 60, "image_url": "images/vanilla cupcake.webp",
     "description": "Sweet vanilla frosted cupcake"},
    
    # Meat & Seafood
    {"name": "Chicken Breast", "category": "Meat", "price": 7.60, "stock": 50, "image_url": "images/chicken breast.webp",
     "description": "Boneless chicken breast"},
    {"name": "Fish Fillet", "category": "Meat", "price": 8.30, "stock": 40, "image_url": "images/fish fillet.webp",
     "description": "Fresh white fish fillet"},
    {"name": "Mutton Cuts", "category": "Meat", "price": 11.20, "stock": 30, "image_url": "images/mutton cuts.webp",
     "description": "Premium mutton cuts"},
    {"name": "Salmon Steak", "category": "Meat", "price": 9.80, "stock": 35, "image_url": "images/salmon steak.webp",
     "description": "Fresh Atlantic salmon"},
    {"name": "Shrimp Basket", "category": "Meat", "price": 8.10, "stock": 45, "image_url": "images/shrimp basket.webp",
     "description": "Jumbo shrimp selection"},
    {"name": "Turkey Bacon", "category": "Meat", "price": 5.90, "stock": 60, "image_url": "images/turkey bacon.webp",
     "description": "Lean turkey bacon strips"},
    
    # Grains
    {"name": "Basmati Rice", "category": "Grains", "price": 5.10, "stock": 100, "image_url": "images/basmati rice.webp",
     "description": "Premium aged basmati rice"},
    {"name": "Whole Wheat Pasta", "category": "Grains", "price": 3.00, "stock": 80, "image_url": "images/whole wheat pasta.webp",
     "description": "Healthy whole wheat pasta"},
    {"name": "Quinoa Pack", "category": "Grains", "price": 4.30, "stock": 70, "image_url": "images/quinoa pack.webp",
     "description": "Organic quinoa grains"},
    {"name": "Rolled Oats", "category": "Grains", "price": 3.20, "stock": 90, "image_url": "images/rolled oats.webp",
     "description": "Premium rolled oats"},
    {"name": "Wheat Grains", "category": "Grains", "price": 3.10, "stock": 85, "image_url": "images/wheat grains.webp",
     "description": "Whole wheat grains"},
    {"name": "Cornmeal", "category": "Grains", "price": 2.70, "stock": 75, "image_url": "images/corn meal.webp",
     "description": "Fine ground cornmeal"},
    
    # Vegetables
    {"name": "Lettuce Head", "category": "Vegetable", "price": 1.25, "stock": 80, "image_url": "images/lettuce head.webp",
     "description": "Fresh iceberg lettuce"},
    {"name": "Cabbage", "category": "Vegetable", "price": 0.95, "stock": 100, "image_url": "images/cabbage.webp",
     "description": "Fresh green cabbage"},
    {"name": "Carrot Bunch", "category": "Vegetable", "price": 0.70, "stock": 120, "image_url": "images/carrot bunch.webp",
     "description": "Fresh organic carrots"},
    {"name": "Onion Bag", "category": "Vegetable", "price": 0.55, "stock": 150, "image_url": "images/onion bag.webp",
     "description": "Red onion bag (1 kg)"},
    {"name": "Garlic Bulb", "category": "Vegetable", "price": 1.50, "stock": 100, "image_url": "images/garlic bulb.webp",
     "description": "Fresh garlic bulbs"},
    {"name": "Green Peas", "category": "Vegetable", "price": 1.35, "stock": 90, "image_url": "images/green peas.webp",
     "description": "Fresh green peas"},
    {"name": "Sweet Corn", "category": "Vegetable", "price": 1.00, "stock": 85, "image_url": "images/sweet corn.webp",
     "description": "Sweet corn on the cob"},
    {"name": "Tomato", "category": "Vegetable", "price": 1.10, "stock": 130, "image_url": "images/tomato.webp",
     "description": "Vine-ripened tomatoes"},
    
    # Snacks
    {"name": "Potato Chips", "category": "Snacks", "price": 2.70, "stock": 100, "image_url": "images/potato chis.webp",
     "description": "Crispy salted potato chips"},
    {"name": "Chocolate Bar", "category": "Snacks", "price": 2.30, "stock": 120, "image_url": "images/chocolate bar.webp",
     "description": "Premium dark chocolate bar"},
    {"name": "Butter Cookies", "category": "Snacks", "price": 2.10, "stock": 90, "image_url": "images/butter cookies.webp",
     "description": "Danish butter cookies"},
    {"name": "Trail Mix", "category": "Snacks", "price": 3.40, "stock": 70, "image_url": "images/trail mix.webp",
     "description": "Nuts and dried fruits mix"},
    {"name": "Ice Cream Tub", "category": "Snacks", "price": 4.30, "stock": 50, "image_url": "images/ice cream tub.webp",
     "description": "Vanilla ice cream tub"},
    {"name": "Pretzel Bites", "category": "Snacks", "price": 2.00, "stock": 80, "image_url": "images/pretzel bites.webp",
     "description": "Salted pretzel bites"},
    
    # Pantry
    {"name": "Honey Jar", "category": "Pantry", "price": 6.50, "stock": 60, "image_url": "images/honey jar.webp",
     "description": "Pure natural honey"},
    {"name": "Jam Spread", "category": "Pantry", "price": 3.60, "stock": 70, "image_url": "images/jam spread.webp",
     "description": "Mixed fruit jam"},
    {"name": "Peanut Butter", "category": "Pantry", "price": 5.00, "stock": 80, "image_url": "images/peanut butter.webp",
     "description": "Creamy peanut butter"},
    {"name": "All-Purpose Flour", "category": "Pantry", "price": 3.20, "stock": 100, "image_url": "images/all purpose flour.webp",
     "description": "Premium all-purpose flour"},
    {"name": "Lentils Mix", "category": "Pantry", "price": 2.90, "stock": 90, "image_url": "images/lentils mix.webp",
     "description": "Mixed lentils pack"},
    {"name": "Kidney Beans", "category": "Pantry", "price": 2.70, "stock": 85, "image_url": "images/kidney beans.webp",
     "description": "Red kidney beans"},
    {"name": "Turmeric Powder", "category": "Pantry", "price": 2.20, "stock": 75, "image_url": "images/turmeric powder.webp",
     "description": "Pure turmeric powder"},
    {"name": "Chili Powder", "category": "Pantry", "price": 2.40, "stock": 80, "image_url": "images/chilly powder.webp",
     "description": "Red chili powder"},
    
    # Beverages
    {"name": "Coffee Beans", "category": "Beverage", "price": 7.60, "stock": 60, "image_url": "images/coffee beans.webp",
     "description": "Premium arabica coffee beans"},
    {"name": "Herbal Tea", "category": "Beverage", "price": 4.30, "stock": 80, "image_url": "images/herbal tea.webp",
     "description": "Organic herbal tea bags"},
    {"name": "Juice Box", "category": "Beverage", "price": 3.20, "stock": 100, "image_url": "images/juice box.webp",
     "description": "Fresh fruit juice pack"},
    {"name": "Soft Drink Can", "category": "Beverage", "price": 2.70, "stock": 120, "image_url": "images/soft drink can.webp",
     "description": "Refreshing cola drink"},
    {"name": "Sparkling Soda", "category": "Beverage", "price": 2.00, "stock": 100, "image_url": "images/sparkling soda.webp",
     "description": "Sparkling mineral water"},
    {"name": "Energy Drink", "category": "Beverage", "price": 4.90, "stock": 70, "image_url": "images/energy drinks.webp",
     "description": "Energy boost drink"},
    
    # Household
    {"name": "Shampoo Bottle", "category": "Household", "price": 5.80, "stock": 60, "image_url": "images/home_shampoo.webp",
     "description": "Nourishing hair shampoo"},
    {"name": "Body Soap", "category": "Household", "price": 1.30, "stock": 100, "image_url": "images/home_soap.webp",
     "description": "Moisturizing bar soap"},
    {"name": "Laundry Detergent", "category": "Household", "price": 6.60, "stock": 50, "image_url": "images/home_detergent.webp",
     "description": "Concentrated laundry detergent"},
    {"name": "Toothpaste Tube", "category": "Household", "price": 2.40, "stock": 80, "image_url": "images/home_toothpaste.webp",
     "description": "Whitening toothpaste"},
    {"name": "Paper Towels", "category": "Household", "price": 3.90, "stock": 70, "image_url": "images/home_paper.webp",
     "description": "Absorbent paper towels roll"},
    {"name": "Dish Soap", "category": "Household", "price": 2.80, "stock": 90, "image_url": "images/home_dishsoap.webp",
     "description": "Grease-cutting dish soap"},
]


def refresh_products():
    """Delete all products and add fresh ones"""
    app = create_app()
    
    with app.app_context():
        print("=" * 50)
        print("REFRESHING PRODUCT DATABASE")
        print("=" * 50)
        
        # Count existing products
        existing_count = Product.query.count()
        print(f"\n📦 Found {existing_count} existing products")
        
        # Clear related tables first (to avoid foreign key issues)
        print("\n🧹 Clearing related data...")
        cart_deleted = CartItem.query.delete()
        print(f"   - Deleted {cart_deleted} cart items")
        
        wishlist_deleted = Wishlist.query.delete()
        print(f"   - Deleted {wishlist_deleted} wishlist items")
        
        review_deleted = Review.query.delete()
        print(f"   - Deleted {review_deleted} reviews")
        
        # Delete order items (keep orders for history)
        # Note: We're keeping orders but clearing product references
        
        # Delete all products
        print("\n🗑️  Deleting existing products...")
        Product.query.delete()
        db.session.commit()
        print(f"   - Deleted {existing_count} products")
        
        # Add new products
        print("\n✨ Adding fresh products...")
        added_count = 0
        categories = {}
        
        for product_data in FRESH_PRODUCTS:
            product = Product(
                name=product_data["name"],
                category=product_data["category"],
                price=product_data["price"],
                stock=product_data["stock"],
                image_url=product_data["image_url"],
                description=product_data.get("description", ""),
                average_rating=0.0,
                review_count=0
            )
            db.session.add(product)
            added_count += 1
            
            # Track categories
            cat = product_data["category"]
            categories[cat] = categories.get(cat, 0) + 1
        
        db.session.commit()
        
        print(f"\n✅ Successfully added {added_count} products!")
        print("\n📊 Products by category:")
        for cat, count in sorted(categories.items()):
            print(f"   - {cat}: {count} products")
        
        print("\n" + "=" * 50)
        print("PRODUCT REFRESH COMPLETE!")
        print("=" * 50)


if __name__ == "__main__":
    refresh_products()

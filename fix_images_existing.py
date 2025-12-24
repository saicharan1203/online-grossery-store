from app import create_app
from extensions import db
from models import Product

app = create_app()

# Map products to EXISTING images only
# Using the category-based images we actually have
product_image_mapping = {
    # Fruits - use existing fruit images
    "Apple": "images/apple.png",
    "Banana": "images/banana.png",
    "Mango": "images/mango.png",
    "Pineapple": "images/fruit.png",
    "Coconut": "images/coconut.png",
    "Strawberry": "images/strawberry.png",
    "Watermelon Slice": "images/watermelon.png",
    
    # Dairy - use generic dairy image
    "Fresh Milk": "images/dairy.png",
    "Greek Yogurt": "images/dairy.png",
    "Butter Slab": "images/dairy.png",
    "Aged Cheese": "images/dairy.png",
    "Paneer Cubes": "images/dairy.png",
    "Curds Cup": "images/dairy.png",
    "Milk": "images/dairy.png",
    "Eggs": "images/dairy.png",
    
    # Bakery - use generic bakery image
    "Sourdough Bread": "images/bakery.png",
    "Butter Croissant": "images/bakery.png",
    "Chocolate Muffin": "images/bakery.png",
    "Cinnamon Roll": "images/bakery.png",
    "Wholegrain Bagel": "images/bakery.png",
    "Vanilla Cupcake": "images/bakery.png",
    "Bread": "images/bakery.png",
    
    # Meat - use dairy as placeholder (similar packaging)
    "Chicken Breast": "images/dairy.png",
    "Fish Fillet": "images/dairy.png",
    "Mutton Cuts": "images/dairy.png",
    "Salmon Steak": "images/dairy.png",
    "Shrimp Basket": "images/dairy.png",
    "Turkey Bacon": "images/dairy.png",
    
    # Grains - use bakery as placeholder
    "Basmati Rice": "images/bakery.png",
    "Whole Wheat Pasta": "images/bakery.png",
    "Quinoa Pack": "images/bakery.png",
    "Rolled Oats": "images/bakery.png",
    "Wheat Grains": "images/bakery.png",
    "Cornmeal": "images/bakery.png",
    "Rice": "images/bakery.png",
    
    # Vegetables - use generic vegetable image
    "Lettuce Head": "images/vegetable.png",
    "Cabbage": "images/vegetable.png",
    "Carrot Bunch": "images/vegetable.png",
    "Onion Bag": "images/vegetable.png",
    "Garlic Bulb": "images/vegetable.png",
    "Green Peas": "images/vegetable.png",
    "Sweet Corn": "images/vegetable.png",
    "Tomato": "images/vegetable.png",
    
    # Snacks - use bakery as placeholder
    "Potato Chips": "images/bakery.png",
    "Chocolate Bar": "images/bakery.png",
    "Butter Cookies": "images/bakery.png",
    "Trail Mix": "images/bakery.png",
    "Ice Cream Tub": "images/bakery.png",
    "Pretzel Bites": "images/bakery.png",
    
    # Pantry - use vegetable as placeholder
    "Honey Jar": "images/vegetable.png",
    "Jam Spread": "images/vegetable.png",
    "Peanut Butter": "images/vegetable.png",
    "All-Purpose Flour": "images/vegetable.png",
    "Lentils Mix": "images/vegetable.png",
    "Kidney Beans": "images/vegetable.png",
    "Turmeric Powder": "images/vegetable.png",
    "Chili Powder": "images/vegetable.png",
    
    # Beverages - use fruit as placeholder
    "Coffee Beans": "images/fruit.png",
    "Herbal Tea": "images/fruit.png",
    "Juice Box": "images/fruit.png",
    "Soft Drink Can": "images/fruit.png",
    "Sparkling Soda": "images/fruit.png",
    "Energy Drink": "images/fruit.png",
    
    # Household - use actual generated images
    "Shampoo Bottle": "images/home_shampoo.png",
    "Body Soap": "images/home_soap.png",
    "Laundry Detergent": "images/home_detergent.png",
    "Toothpaste Tube": "images/home_toothpaste.png",
    "Paper Towels": "images/home_paper.png",
    "Dish Soap": "images/home_dishsoap.png",
}

with app.app_context():
    print("=" * 70)
    print("UPDATING PRODUCTS WITH EXISTING IMAGES ONLY")
    print("=" * 70)
    
    updated = 0
    
    for product_name, image_path in product_image_mapping.items():
        product = Product.query.filter_by(name=product_name).first()
        if product:
            old_path = product.image_url
            product.image_url = image_path
            print(f"✓ {product_name:30} → {image_path}")
            updated += 1
    
    db.session.commit()
    
    print("=" * 70)
    print(f"✅ Successfully updated {updated} products with existing images!")
    print("=" * 70)

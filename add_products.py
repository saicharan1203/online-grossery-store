from app import create_app
from extensions import db
from models import Product

app = create_app()

products_to_add = [
    # Fruit
    {"name": "Apple", "category": "Fruit", "image_url": "images/apple.png", "price": 1.20},
    {"name": "Banana", "category": "Fruit", "image_url": "images/banana.png", "price": 0.55},
    {"name": "Mango", "category": "Fruit", "image_url": "images/mango.png", "price": 1.80},
    {"name": "Pineapple", "category": "Fruit", "image_url": "images/pineapple.png", "price": 2.40},
    {"name": "Coconut", "category": "Fruit", "image_url": "images/coconut.png", "price": 2.10},
    {"name": "Strawberry", "category": "Fruit", "image_url": "images/strawberry.png", "price": 2.90},
    {"name": "Watermelon Slice", "category": "Fruit", "image_url": "images/watermelon.png", "price": 4.60},

    # Dairy
    {"name": "Fresh Milk", "category": "Dairy", "image_url": "images/dairy_milk.png", "price": 3.40},
    {"name": "Greek Yogurt", "category": "Dairy", "image_url": "images/dairy_yogurt.png", "price": 2.10},
    {"name": "Butter Slab", "category": "Dairy", "image_url": "images/dairy_butter.png", "price": 2.60},
    {"name": "Aged Cheese", "category": "Dairy", "image_url": "images/dairy_cheese.png", "price": 4.80},
    {"name": "Paneer Cubes", "category": "Dairy", "image_url": "images/dairy_paneer.png", "price": 3.70},
    {"name": "Curds Cup", "category": "Dairy", "image_url": "images/dairy_curds.png", "price": 1.90},

    # Bakery
    {"name": "Sourdough Bread", "category": "Bakery", "image_url": "images/bakery_sourdough.png", "price": 3.30},
    {"name": "Butter Croissant", "category": "Bakery", "image_url": "images/bakery_croissant.png", "price": 1.70},
    {"name": "Chocolate Muffin", "category": "Bakery", "image_url": "images/bakery_muffin.png", "price": 2.20},
    {"name": "Cinnamon Roll", "category": "Bakery", "image_url": "images/bakery_cinnamon.png", "price": 2.80},
    {"name": "Wholegrain Bagel", "category": "Bakery", "image_url": "images/bakery_bagel.png", "price": 1.40},
    {"name": "Vanilla Cupcake", "category": "Bakery", "image_url": "images/bakery_cupcake.png", "price": 2.60},

    # Meat
    {"name": "Chicken Breast", "category": "Meat", "image_url": "images/meat_chicken.png", "price": 7.60},
    {"name": "Fish Fillet", "category": "Meat", "image_url": "images/meat_fish.png", "price": 8.30},
    {"name": "Mutton Cuts", "category": "Meat", "image_url": "images/meat_mutton.png", "price": 11.20},
    {"name": "Salmon Steak", "category": "Meat", "image_url": "images/meat_salmon.png", "price": 9.80},
    {"name": "Shrimp Basket", "category": "Meat", "image_url": "images/meat_shrimp.png", "price": 8.10},
    {"name": "Turkey Bacon", "category": "Meat", "image_url": "images/meat_turkey.png", "price": 5.90},

    # Grains
    {"name": "Basmati Rice", "category": "Grains", "image_url": "images/grains_rice.png", "price": 5.10},
    {"name": "Whole Wheat Pasta", "category": "Grains", "image_url": "images/grains_pasta.png", "price": 3.00},
    {"name": "Quinoa Pack", "category": "Grains", "image_url": "images/grains_quinoa.png", "price": 4.30},
    {"name": "Rolled Oats", "category": "Grains", "image_url": "images/grains_oats.png", "price": 3.20},
    {"name": "Wheat Grains", "category": "Grains", "image_url": "images/grains_wheat.png", "price": 3.10},
    {"name": "Cornmeal", "category": "Grains", "image_url": "images/grains_cornmeal.png", "price": 2.70},

    # Vegetable
    {"name": "Lettuce Head", "category": "Vegetable", "image_url": "images/veg_lettuce.png", "price": 1.25},
    {"name": "Cabbage", "category": "Vegetable", "image_url": "images/veg_cabbage.png", "price": 0.95},
    {"name": "Carrot Bunch", "category": "Vegetable", "image_url": "images/veg_carrot.png", "price": 0.70},
    {"name": "Onion Bag", "category": "Vegetable", "image_url": "images/veg_onion.png", "price": 0.55},
    {"name": "Garlic Bulb", "category": "Vegetable", "image_url": "images/veg_garlic.png", "price": 1.50},
    {"name": "Green Peas", "category": "Vegetable", "image_url": "images/veg_peas.png", "price": 1.35},
    {"name": "Sweet Corn", "category": "Vegetable", "image_url": "images/veg_corn.png", "price": 1.00},

    # Snacks
    {"name": "Potato Chips", "category": "Snacks", "image_url": "images/snack_chips.png", "price": 2.70},
    {"name": "Chocolate Bar", "category": "Snacks", "image_url": "images/snack_chocolate.png", "price": 2.30},
    {"name": "Butter Cookies", "category": "Snacks", "image_url": "images/snack_cookies.png", "price": 2.10},
    {"name": "Trail Mix", "category": "Snacks", "image_url": "images/snack_trailmix.png", "price": 3.40},
    {"name": "Ice Cream Tub", "category": "Snacks", "image_url": "images/snack_icecream.png", "price": 4.30},
    {"name": "Pretzel Bites", "category": "Snacks", "image_url": "images/snack_pretzel.png", "price": 2.00},

    # Pantry
    {"name": "Honey Jar", "category": "Pantry", "image_url": "images/pantry_honey.png", "price": 6.50},
    {"name": "Jam Spread", "category": "Pantry", "image_url": "images/pantry_jam.png", "price": 3.60},
    {"name": "Peanut Butter", "category": "Pantry", "image_url": "images/pantry_peanut.png", "price": 5.00},
    {"name": "All-Purpose Flour", "category": "Pantry", "image_url": "images/pantry_flour.png", "price": 3.20},
    {"name": "Lentils Mix", "category": "Pantry", "image_url": "images/pantry_lentils.png", "price": 2.90},
    {"name": "Kidney Beans", "category": "Pantry", "image_url": "images/pantry_beans.png", "price": 2.70},
    {"name": "Turmeric Powder", "category": "Pantry", "image_url": "images/pantry_turmeric.png", "price": 2.20},
    {"name": "Chili Powder", "category": "Pantry", "image_url": "images/pantry_chili.png", "price": 2.40},

    # Beverage
    {"name": "Coffee Beans", "category": "Beverage", "image_url": "images/bev_coffee.png", "price": 7.60},
    {"name": "Herbal Tea", "category": "Beverage", "image_url": "images/bev_tea.png", "price": 4.30},
    {"name": "Juice Box", "category": "Beverage", "image_url": "images/bev_juice.png", "price": 3.20},
    {"name": "Soft Drink Can", "category": "Beverage", "image_url": "images/bev_softdrink.png", "price": 2.70},
    {"name": "Sparkling Soda", "category": "Beverage", "image_url": "images/bev_soda.png", "price": 2.00},
    {"name": "Energy Drink", "category": "Beverage", "image_url": "images/bev_energy.png", "price": 4.90},

    # Household
    {"name": "Shampoo Bottle", "category": "Household", "image_url": "images/home_shampoo.png", "price": 5.80},
    {"name": "Body Soap", "category": "Household", "image_url": "images/home_soap.png", "price": 1.30},
    {"name": "Laundry Detergent", "category": "Household", "image_url": "images/home_detergent.png", "price": 6.60},
    {"name": "Toothpaste Tube", "category": "Household", "image_url": "images/home_toothpaste.png", "price": 2.40},
    {"name": "Paper Towels", "category": "Household", "image_url": "images/home_paper.png", "price": 3.90},
    {"name": "Dish Soap", "category": "Household", "image_url": "images/home_dishsoap.png", "price": 2.80},
]

with app.app_context():
    print(f"Adding {len(products_to_add)} products...")
    added_count = 0
    for item in products_to_add:
        # Check if product already exists
        existing_product = Product.query.filter_by(name=item['name']).first()
        if not existing_product:
            new_product = Product(
                name=item['name'],
                category=item['category'],
                price=item['price'],
                image_url=item['image_url'],
                stock=100  # Default stock
            )
            db.session.add(new_product)
            added_count += 1
        else:
            # Update existing product to match user request
            existing_product.category = item['category']
            existing_product.price = item['price']
            existing_product.image_url = item['image_url']
            print(f"Updated existing product: {item['name']}")
    
    db.session.commit()
    print(f"Successfully added {added_count} new products.")

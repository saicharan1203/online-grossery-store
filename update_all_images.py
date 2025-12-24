from app import create_app
from extensions import db
from models import Product

app = create_app()

# Complete product image mapping from add_products.py
product_images = {
    # Fruit
    "Apple": "images/apple.png",
    "Banana": "images/banana.png",
    "Mango": "images/mango.png",
    "Pineapple": "images/pineapple.png",
    "Coconut": "images/coconut.png",
    "Strawberry": "images/strawberry.png",
    "Watermelon Slice": "images/watermelon.png",
    
    # Dairy
    "Fresh Milk": "images/dairy_milk.png",
    "Greek Yogurt": "images/dairy_yogurt.png",
    "Butter Slab": "images/dairy_butter.png",
    "Aged Cheese": "images/dairy_cheese.png",
    "Paneer Cubes": "images/dairy_paneer.png",
    "Curds Cup": "images/dairy_curds.png",
    "Milk": "images/dairy_milk.png",
    "Eggs": "images/dairy_eggs.png",
    
    # Bakery
    "Sourdough Bread": "images/bakery_sourdough.png",
    "Butter Croissant": "images/bakery_croissant.png",
    "Chocolate Muffin": "images/bakery_muffin.png",
    "Cinnamon Roll": "images/bakery_cinnamon.png",
    "Wholegrain Bagel": "images/bakery_bagel.png",
    "Vanilla Cupcake": "images/bakery_cupcake.png",
    "Bread": "images/bakery_sourdough.png",
    
    # Meat
    "Chicken Breast": "images/meat_chicken.png",
    "Fish Fillet": "images/meat_fish.png",
    "Mutton Cuts": "images/meat_mutton.png",
    "Salmon Steak": "images/meat_salmon.png",
    "Shrimp Basket": "images/meat_shrimp.png",
    "Turkey Bacon": "images/meat_turkey.png",
    
    # Grains
    "Basmati Rice": "images/grains_rice.png",
    "Whole Wheat Pasta": "images/grains_pasta.png",
    "Quinoa Pack": "images/grains_quinoa.png",
    "Rolled Oats": "images/grains_oats.png",
    "Wheat Grains": "images/grains_wheat.png",
    "Cornmeal": "images/grains_cornmeal.png",
    "Rice": "images/grains_rice.png",
    
    # Vegetable
    "Lettuce Head": "images/veg_lettuce.png",
    "Cabbage": "images/veg_cabbage.png",
    "Carrot Bunch": "images/veg_carrot.png",
    "Onion Bag": "images/veg_onion.png",
    "Garlic Bulb": "images/veg_garlic.png",
    "Green Peas": "images/veg_peas.png",
    "Sweet Corn": "images/veg_corn.png",
    "Tomato": "images/veg_tomato.png",
    
    # Snacks
    "Potato Chips": "images/snack_chips.png",
    "Chocolate Bar": "images/snack_chocolate.png",
    "Butter Cookies": "images/snack_cookies.png",
    "Trail Mix": "images/snack_trailmix.png",
    "Ice Cream Tub": "images/snack_icecream.png",
    "Pretzel Bites": "images/snack_pretzel.png",
    
    # Pantry
    "Honey Jar": "images/pantry_honey.png",
    "Jam Spread": "images/pantry_jam.png",
    "Peanut Butter": "images/pantry_peanut.png",
    "All-Purpose Flour": "images/pantry_flour.png",
    "Lentils Mix": "images/pantry_lentils.png",
    "Kidney Beans": "images/pantry_beans.png",
    "Turmeric Powder": "images/pantry_turmeric.png",
    "Chili Powder": "images/pantry_chili.png",
    
    # Beverage
    "Coffee Beans": "images/bev_coffee.png",
    "Herbal Tea": "images/bev_tea.png",
    "Juice Box": "images/bev_juice.png",
    "Soft Drink Can": "images/bev_softdrink.png",
    "Sparkling Soda": "images/bev_soda.png",
    "Energy Drink": "images/bev_energy.png",
    
    # Household
    "Shampoo Bottle": "images/home_shampoo.png",
    "Body Soap": "images/home_soap.png",
    "Laundry Detergent": "images/home_detergent.png",
    "Toothpaste Tube": "images/home_toothpaste.png",
    "Paper Towels": "images/home_paper.png",
    "Dish Soap": "images/home_dishsoap.png",
}

with app.app_context():
    print("=" * 60)
    print("UPDATING ALL PRODUCT IMAGES")
    print("=" * 60)
    
    updated_count = 0
    not_found_count = 0
    already_correct = 0
    
    for product_name, correct_image in product_images.items():
        product = Product.query.filter_by(name=product_name).first()
        if product:
            if product.image_url != correct_image:
                old_image = product.image_url
                product.image_url = correct_image
                print(f"✓ {product_name:25} {old_image:30} → {correct_image}")
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
    if not_found_count > 0:
        print(f"⚠  Not found: {not_found_count} products")
    print("=" * 60)
    print("\n🎉 Database update complete!")

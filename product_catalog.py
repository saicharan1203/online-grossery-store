from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Product:
    name: str
    category: str
    image_url: str
    price: float


PRODUCTS: List[Product] = [
    Product("Apple", "Fruit", "images/apple.png", 1.20),
    Product("Banana", "Fruit", "images/banana.png", 0.55),
    Product("Mango", "Fruit", "images/mango.png", 1.80),
    Product("Pineapple", "Fruit", "images/pineapple.png", 2.40),
    Product("Coconut", "Fruit", "images/coconut.png", 2.10),
    Product("Strawberry", "Fruit", "images/strawberry.png", 2.90),
    Product("Watermelon Slice", "Fruit", "images/watermelon.png", 4.60),
    Product("Fresh Milk", "Dairy", "images/fresh milk.webp", 3.40),
    Product("Greek Yogurt", "Dairy", "images/greek yogurt.webp", 2.10),
    Product("Butter Slab", "Dairy", "images/butter slab.webp", 2.60),
    Product("Aged Cheese", "Dairy", "images/aged cheese.webp", 4.80),
    Product("Paneer Cubes", "Dairy", "images/dairy_paneer.png", 3.70),
    Product("Curds Cup", "Dairy", "images/curds cup.webp", 1.90),
    Product("Sourdough Bread", "Bakery", "images/bakery_sourdough.png", 3.30),
    Product("Butter Croissant", "Bakery", "images/butter croissant.webp", 1.70),
    Product("Chocolate Muffin", "Bakery", "images/chocolate muffin.webp", 2.20),
    Product("Cinnamon Roll", "Bakery", "images/cinnamon rolls.webp", 2.80),
    Product("Wholegrain Bagel", "Bakery", "images/bakery_bagel.png", 1.40),
    Product("Vanilla Cupcake", "Bakery", "images/bakery_cupcake.png", 2.60),
    Product("Chicken Breast", "Meat", "images/chicken breast.webp", 7.60),
    Product("Fish Fillet", "Meat", "images/meat_fish.png", 8.30),
    Product("Mutton Cuts", "Meat", "images/meat_mutton.png", 11.20),
    Product("Salmon Steak", "Meat", "images/meat_salmon.png", 9.80),
    Product("Shrimp Basket", "Meat", "images/meat_shrimp.png", 8.10),
    Product("Turkey Bacon", "Meat", "images/meat_turkey.png", 5.90),
    Product("Basmati Rice", "Grains", "images/basmati rice.webp", 5.10),
    Product("Whole Wheat Pasta", "Grains", "images/grains_pasta.png", 3.00),
    Product("Quinoa Pack", "Grains", "images/grains_quinoa.png", 4.30),
    Product("Rolled Oats", "Grains", "images/grains_oats.png", 3.20),
    Product("Wheat Grains", "Grains", "images/grains_wheat.png", 3.10),
    Product("Cornmeal", "Grains", "images/corn meal.webp", 2.70),
    Product("Rice", "Grains", "images/grains_rice.png", 4.80),
    Product("Lettuce Head", "Vegetable", "images/veg_lettuce.png", 1.25),
    Product("Cabbage", "Vegetable", "images/cabbage.webp", 0.95),
    Product("Carrot Bunch", "Vegetable", "images/carrot bunch.webp", 0.70),
    Product("Onion Bag", "Vegetable", "images/veg_onion.png", 0.55),
    Product("Garlic Bulb", "Vegetable", "images/garlic bulb.webp", 1.50),
    Product("Green Peas", "Vegetable", "images/veg_peas.png", 1.35),
    Product("Sweet Corn", "Vegetable", "images/veg_corn.png", 1.00),
    Product("Tomato", "Vegetable", "images/veg_tomato.png", 1.10),
    Product("Potato Chips", "Snacks", "images/snack_chips.png", 2.70),
    Product("Chocolate Bar", "Snacks", "images/snack_chocolate.png", 2.30),
    Product("Butter Cookies", "Snacks", "images/butter cookies.webp", 2.10),
    Product("Trail Mix", "Snacks", "images/snack_trailmix.png", 3.40),
    Product("Ice Cream Tub", "Snacks", "images/snack_icecream.png", 4.30),
    Product("Pretzel Bites", "Snacks", "images/snack_pretzel.png", 2.00),
    Product("Honey Jar", "Pantry", "images/honey jar.webp", 6.50),
    Product("Jam Spread", "Pantry", "images/pantry_jam.png", 3.60),
    Product("Peanut Butter", "Pantry", "images/pantry_peanut.png", 5.00),
    Product("All-Purpose Flour", "Pantry", "images/pantry_flour.png", 3.20),
    Product("Lentils Mix", "Pantry", "images/pantry_lentils.png", 2.90),
    Product("Kidney Beans", "Pantry", "images/pantry_beans.png", 2.70),
    Product("Turmeric Powder", "Pantry", "images/pantry_turmeric.png", 2.20),
    Product("Chili Powder", "Pantry", "images/chilly powder.webp", 2.40),
    Product("Coffee Beans", "Beverage", "images/coffee beans.webp", 7.60),
    Product("Herbal Tea", "Beverage", "images/herbal tea.webp", 4.30),
    Product("Juice Box", "Beverage", "images/bev_juice.png", 3.20),
    Product("Soft Drink Can", "Beverage", "images/bev_softdrink.png", 2.70),
    Product("Sparkling Soda", "Beverage", "images/bev_soda.png", 2.00),
    Product("Energy Drink", "Beverage", "images/energy drinks.webp", 4.90),
    Product("Shampoo Bottle", "Household", "images/home_shampoo.png", 5.80),
    Product("Body Soap", "Household", "images/home_soap.png", 1.30),
    Product("Laundry Detergent", "Household", "images/home_detergent.png", 6.60),
    Product("Toothpaste Tube", "Household", "images/home_toothpaste.png", 2.40),
    Product("Paper Towels", "Household", "images/home_paper.png", 3.90),
    Product("Dish Soap", "Household", "images/home_dishsoap.png", 2.80),
]

ADDITIONAL_IMAGE_OVERRIDES = {
    "Milk": ("Dairy", "images/dairy_milk.png"),
    "Eggs": ("Dairy", "images/dairy_eggs.png"),
}

CATEGORY_FALLBACKS: Dict[str, str] = {
    "Fruit": "images/fruit.png",
    "Dairy": "images/dairy.png",
    "Bakery": "images/bakery.png",
    "Vegetable": "images/vegetable.png",
    "Grains": "images/bakery.png",
    "Meat": "images/dairy.png",
    "Snacks": "images/bakery.png",
    "Pantry": "images/vegetable.png",
    "Beverage": "images/fruit.png",
    "Household": "images/home_paper.png",
}

PRODUCT_IMAGE_MAP: Dict[str, str] = {product.name: product.image_url for product in PRODUCTS}
for extra_name, (category, image) in ADDITIONAL_IMAGE_OVERRIDES.items():
    PRODUCT_IMAGE_MAP.setdefault(extra_name, image)

PRODUCT_CATEGORY_MAP: Dict[str, str] = {product.name: product.category for product in PRODUCTS}
for extra_name, (category, _image) in ADDITIONAL_IMAGE_OVERRIDES.items():
    PRODUCT_CATEGORY_MAP.setdefault(extra_name, category)


PRODUCT_THEMES: Dict[str, Dict[str, str]] = {
    # Fruit
    "Apple": {"shape": "round_leaf", "primary": "#ff6b6b", "secondary": "#ff9372"},
    "Banana": {"shape": "banana", "primary": "#fddb5c", "secondary": "#f6b93b"},
    "Mango": {"shape": "round_leaf", "primary": "#ff9b42", "secondary": "#ffbd5a"},
    "Pineapple": {"shape": "pineapple", "primary": "#fcca55", "secondary": "#d38b29"},
    "Coconut": {"shape": "coconut", "primary": "#6f4e37", "secondary": "#a67c52"},
    "Strawberry": {"shape": "berry", "primary": "#ff4d6d", "secondary": "#ff758f"},
    "Watermelon Slice": {"shape": "watermelon", "primary": "#ff6b6b", "secondary": "#1dd3b0"},
    # Dairy
    "Fresh Milk": {"shape": "carton", "primary": "#7bc4ff", "secondary": "#e3f2ff"},
    "Greek Yogurt": {"shape": "cup", "primary": "#b6d9ff", "secondary": "#f3f7ff"},
    "Butter Slab": {"shape": "block", "primary": "#ffd166", "secondary": "#ffaf45"},
    "Aged Cheese": {"shape": "wedge", "primary": "#ffc55c", "secondary": "#ffe08a"},
    "Paneer Cubes": {"shape": "cube", "primary": "#f6f2e6", "secondary": "#d8e2dc"},
    "Curds Cup": {"shape": "cup", "primary": "#e4f1ff", "secondary": "#c6dce4"},
    "Milk": {"shape": "carton", "primary": "#9fd3ff", "secondary": "#ffffff"},
    "Eggs": {"shape": "eggs", "primary": "#fff5d7", "secondary": "#f2d5b3"},
    # Bakery
    "Sourdough Bread": {"shape": "loaf", "primary": "#f4a261", "secondary": "#d48c50"},
    "Butter Croissant": {"shape": "croissant", "primary": "#ffbe76", "secondary": "#f6a25c"},
    "Chocolate Muffin": {"shape": "muffin", "primary": "#a0522d", "secondary": "#c77b57"},
    "Cinnamon Roll": {"shape": "spiral", "primary": "#d7996b", "secondary": "#f4c095"},
    "Wholegrain Bagel": {"shape": "bagel", "primary": "#f0b67f", "secondary": "#d08c60"},
    "Vanilla Cupcake": {"shape": "cupcake", "primary": "#ffddd2", "secondary": "#fcbf49"},
    "Bread": {"shape": "loaf", "primary": "#f3b98f", "secondary": "#d19168"},
    # Meat
    "Chicken Breast": {"shape": "steak", "primary": "#ffb3a7", "secondary": "#ff8a80"},
    "Fish Fillet": {"shape": "fish", "primary": "#64c5ff", "secondary": "#3a86ff"},
    "Mutton Cuts": {"shape": "meat_cut", "primary": "#d62839", "secondary": "#a4133c"},
    "Salmon Steak": {"shape": "salmon", "primary": "#ff9770", "secondary": "#ff6b6b"},
    "Shrimp Basket": {"shape": "shrimp", "primary": "#ff8fab", "secondary": "#ff99c8"},
    "Turkey Bacon": {"shape": "bacon", "primary": "#f4a7bb", "secondary": "#d88c9a"},
    # Grains
    "Basmati Rice": {"shape": "bag", "primary": "#f2e9e4", "secondary": "#c9ada7"},
    "Whole Wheat Pasta": {"shape": "box", "primary": "#f4d58d", "secondary": "#d4a373"},
    "Quinoa Pack": {"shape": "bag", "primary": "#f7ede2", "secondary": "#e9c46a"},
    "Rolled Oats": {"shape": "bowl", "primary": "#fff1c1", "secondary": "#e9c46a"},
    "Wheat Grains": {"shape": "bundle", "primary": "#f2c57c", "secondary": "#d97b66"},
    "Cornmeal": {"shape": "scoop", "primary": "#ffe066", "secondary": "#f4a261"},
    "Rice": {"shape": "bowl", "primary": "#fefae0", "secondary": "#ccd5ae"},
    # Vegetables
    "Lettuce Head": {"shape": "leafy", "primary": "#80ed99", "secondary": "#57cc99"},
    "Cabbage": {"shape": "leafy", "primary": "#a3b18a", "secondary": "#588157"},
    "Carrot Bunch": {"shape": "carrot", "primary": "#f4a261", "secondary": "#2a9d8f"},
    "Onion Bag": {"shape": "bulb", "primary": "#f7cad0", "secondary": "#e2a0b1"},
    "Garlic Bulb": {"shape": "garlic", "primary": "#f8edeb", "secondary": "#e3d5ca"},
    "Green Peas": {"shape": "pod", "primary": "#99d98c", "secondary": "#76c893"},
    "Sweet Corn": {"shape": "corn", "primary": "#ffd166", "secondary": "#70e000"},
    "Tomato": {"shape": "round_leaf", "primary": "#ef233c", "secondary": "#ff595e"},
    # Snacks
    "Potato Chips": {"shape": "chips", "primary": "#ffe066", "secondary": "#ffba08"},
    "Chocolate Bar": {"shape": "bar", "primary": "#7f5539", "secondary": "#a47148"},
    "Butter Cookies": {"shape": "cookies", "primary": "#f4a261", "secondary": "#f6bd60"},
    "Trail Mix": {"shape": "mix_bowl", "primary": "#cdb4db", "secondary": "#ffc8dd"},
    "Ice Cream Tub": {"shape": "tub", "primary": "#ffcad4", "secondary": "#bde0fe"},
    "Pretzel Bites": {"shape": "pretzel", "primary": "#d08c60", "secondary": "#bc6c25"},
    # Pantry
    "Honey Jar": {"shape": "jar", "primary": "#ffbe0b", "secondary": "#f48c06"},
    "Jam Spread": {"shape": "jar", "primary": "#ff87ab", "secondary": "#ff5d8f"},
    "Peanut Butter": {"shape": "jar", "primary": "#f4a261", "secondary": "#e76f51"},
    "All-Purpose Flour": {"shape": "bag", "primary": "#f9f7f3", "secondary": "#c9ada7"},
    "Lentils Mix": {"shape": "bag", "primary": "#f4a261", "secondary": "#e76f51"},
    "Kidney Beans": {"shape": "bag", "primary": "#b23a48", "secondary": "#780000"},
    "Turmeric Powder": {"shape": "jar", "primary": "#f6aa1c", "secondary": "#f3722c"},
    "Chili Powder": {"shape": "jar", "primary": "#ef233c", "secondary": "#d62828"},
    # Beverage
    "Coffee Beans": {"shape": "bag", "primary": "#6f4e37", "secondary": "#a47148"},
    "Herbal Tea": {"shape": "box", "primary": "#95d5b2", "secondary": "#52b788"},
    "Juice Box": {"shape": "juice_box", "primary": "#ff9b85", "secondary": "#ffb5a7"},
    "Soft Drink Can": {"shape": "can", "primary": "#ef476f", "secondary": "#ffd166"},
    "Sparkling Soda": {"shape": "bottle", "primary": "#4cc9f0", "secondary": "#4895ef"},
    "Energy Drink": {"shape": "can", "primary": "#ffbe0b", "secondary": "#fb5607"},
    # Household
    "Shampoo Bottle": {"shape": "bottle", "primary": "#b2f7ef", "secondary": "#5dade2"},
    "Body Soap": {"shape": "soap", "primary": "#f7ede2", "secondary": "#f2c6de"},
    "Laundry Detergent": {"shape": "jug", "primary": "#48cae4", "secondary": "#0096c7"},
    "Toothpaste Tube": {"shape": "tube", "primary": "#ade8f4", "secondary": "#caf0f8"},
    "Paper Towels": {"shape": "roll", "primary": "#e9ecef", "secondary": "#ced4da"},
    "Dish Soap": {"shape": "bottle", "primary": "#80ed99", "secondary": "#57cc99"},
}

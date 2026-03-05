"""
FreshMarket AI Shopping Assistant
Uses Google Gemini API (free tier) to power an intelligent grocery chatbot.
Falls back to a rich rule-based engine with live DB data when API is unavailable.
"""

import os
import requests
from models import Product, Order, CartItem
from extensions import db


GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"


# ── DB Helpers ─────────────────────────────────────────────────────────────────

def get_products_by_category(category, limit=20):
    """Return in-stock products for a given category."""
    try:
        return (Product.query
                .filter_by(category=category)
                .filter(Product.stock > 0)
                .order_by(Product.average_rating.desc(), Product.name.asc())
                .limit(limit).all())
    except Exception:
        return []


def get_all_in_stock():
    """Return all in-stock products."""
    try:
        return Product.query.filter(Product.stock > 0).order_by(Product.category, Product.name).all()
    except Exception:
        return []


def get_product_catalog_context():
    """Fetch current product catalog to give AI context about available items."""
    try:
        products = Product.query.filter(Product.stock > 0).all()
        catalog = []
        for p in products:
            catalog.append({
                'name': p.name,
                'category': p.category,
                'price': f"₹{p.price:.2f}",
                'stock': p.stock,
                'rating': f"{p.average_rating:.1f}/5",
                'description': p.description or ''
            })
        return catalog
    except Exception:
        return []


def get_user_order_context(user_id):
    """Fetch user's recent orders for personalized recommendations."""
    try:
        recent_orders = (Order.query.filter_by(user_id=user_id)
                         .order_by(Order.date.desc()).limit(3).all())
        order_data = []
        for order in recent_orders:
            items = [item.product.name for item in order.items if item.product]
            order_data.append({
                'order_id': order.id,
                'date': order.date.strftime('%Y-%m-%d'),
                'status': order.status,
                'items': items,
                'total': f"₹{order.total_price:.2f}"
            })
        return order_data
    except Exception:
        return []


def get_cart_context(user_id):
    """Fetch current cart items for the user."""
    try:
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        cart, total = [], 0
        for item in cart_items:
            if item.product:
                subtotal = item.product.price * item.quantity
                total += subtotal
                cart.append({
                    'name': item.product.name,
                    'quantity': item.quantity,
                    'price': f"₹{item.product.price:.2f}",
                    'subtotal': f"₹{subtotal:.2f}"
                })
        return cart, total
    except Exception:
        return [], 0


# ── Formatter Helpers ──────────────────────────────────────────────────────────

def _fmt_product_row(p, idx=None):
    """Format a single product as a chat-friendly line."""
    stars = "★" * round(p.average_rating) + "☆" * (5 - round(p.average_rating))
    prefix = f"{idx}. " if idx else "• "
    return f"{prefix}**{p.name}** — ₹{p.price:.2f}  {stars} ({p.average_rating:.1f})"


def _fmt_product_list(products, category_label="items"):
    """Return a formatted numbered list string for a list of products."""
    if not products:
        return f"Sorry, we currently have no {category_label} in stock. Check back soon! 🙏"
    lines = [_fmt_product_row(p, i + 1) for i, p in enumerate(products)]
    return "\n".join(lines)


def _add_to_cart_instructions():
    return (
        "\n\n**How to add to cart:**\n"
        "1. Find the item on the homepage or search for it\n"
        "2. Click the 🛒 **Add to Cart** button on the product card\n"
        "3. Go to **Cart** in the navbar → then **Checkout** to place your order"
    )


def _search_instructions(category=""):
    tip = f'Search for "{category}"' if category else "Use the search bar"
    return (
        f"\n\n💡 **Tip:** {tip} on the homepage, or use the **Category filter** "
        "on the left to browse only this section."
    )


# ── Gemini System Prompt ───────────────────────────────────────────────────────

def build_system_prompt(user=None, catalog=None, orders=None, cart=None, cart_total=0):
    """Build a comprehensive system prompt for the AI assistant."""

    catalog_text = ""
    if catalog:
        categories = {}
        for item in catalog:
            cat = item['category']
            categories.setdefault(cat, []).append(
                f"{item['name']} ({item['price']}, ★{item['rating']})"
            )
        catalog_text = "\n\n📦 AVAILABLE PRODUCTS (in stock):\n"
        for cat, items in categories.items():
            catalog_text += f"\n{cat}:\n"
            for item in items[:15]:
                catalog_text += f"  • {item}\n"

    orders_text = ""
    if orders:
        orders_text = "\n\n🛒 USER'S RECENT ORDERS:\n"
        for o in orders:
            orders_text += (
                f"  Order #{o['order_id']} ({o['date']}) — {o['status']}: "
                f"{', '.join(o['items'][:4])}\n"
            )

    cart_text = ""
    if cart:
        cart_text = f"\n\n🛍️ CURRENT CART ({len(cart)} items, Total: ₹{cart_total:.2f}):\n"
        for item in cart:
            cart_text += f"  • {item['name']} x{item['quantity']} = {item['subtotal']}\n"

    username = user.username if user else "Guest"

    return f"""You are FreshBot 🤖, the friendly AI shopping assistant for FreshMarket — an online grocery store in India.

Customer name: {username}
{catalog_text}
{orders_text}
{cart_text}

YOUR CAPABILITIES:
1. 🛒 Product listings & recommendations
2. 🍳 Recipe suggestions using in-stock items
3. 📦 Order/delivery queries
4. 💰 Budget-friendly grocery tips
5. 🥗 Nutrition & healthy eating advice
6. ⭐ Loyalty points & coupon guidance

RESPONSE FORMAT RULES (very important):
- When a user asks "what [category] do you have?" or "list your [category]", ALWAYS:
  a) Give a numbered list of ALL items in that category with price and rating
  b) Follow it with brief instructions on how to add them to cart
  c) End with a helpful tip (recipe idea, nutrition note, etc.)
- Use **bold** for product names and section headers
- Use numbered lists for product catalogs
- Use bullet points for instructions/tips
- Keep responses warm and conversational
- Always quote REAL prices from the catalog above — never make up data
- Support Indian grocery terms: sabzi=vegetable, dal=lentils, atta=flour, etc.
- Maximum response length: aim for clarity, not brevity — users want complete information
"""


# ── Gemini API Call ────────────────────────────────────────────────────────────

def chat_with_ai(message, user=None, conversation_history=None):
    """
    Main function: tries Gemini API first, falls back to rule-based engine.
    """
    if not GEMINI_API_KEY:
        return get_fallback_response(message, user)

    catalog = get_product_catalog_context()
    orders = get_user_order_context(user.id) if user and user.is_authenticated else []
    cart, cart_total = get_cart_context(user.id) if user and user.is_authenticated else ([], 0)

    system_prompt = build_system_prompt(user, catalog, orders, cart, cart_total)

    if conversation_history is None:
        conversation_history = []

    contents = []
    for msg in conversation_history[-10:]:
        contents.append({
            "role": msg["role"],
            "parts": [{"text": msg["content"]}]
        })
    contents.append({"role": "user", "parts": [{"text": message}]})

    payload = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": contents,
        "generationConfig": {
            "temperature": 0.65,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 800,
        },
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT",        "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH",       "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
    }

    try:
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            candidates = data.get('candidates', [])
            if candidates and candidates[0].get('content'):
                text = candidates[0]['content']['parts'][0]['text']
                return text.strip()

        if response.status_code == 429:
            return "⏳ I'm a bit busy right now! Please try again in a moment."

        # Fall through to rule-based
        return get_fallback_response(message, user)

    except requests.exceptions.Timeout:
        return "⏳ That took a bit too long. Please try again!"
    except Exception:
        return get_fallback_response(message, user)


# ── Rule-Based Fallback Engine ─────────────────────────────────────────────────

def get_fallback_response(message, user=None):
    """
    Rich rule-based responses that query the live DB to give real product data.
    Handles category listings, recipes, orders, cart, loyalty, and more.
    """
    ml = message.lower().strip()

    # ── Greetings ──────────────────────────────────────────────────────────────
    greetings = ['hello', 'hi', 'hey', 'namaste', 'good morning', 'good afternoon',
                 'good evening', 'hola', 'howdy', 'sup', 'what\'s up']
    if any(w in ml for w in greetings):
        name = f", {user.username}" if user and user.is_authenticated else ""
        return (
            f"👋 Hello{name}! Welcome to **FreshMarket**! I'm **FreshBot**, your AI grocery assistant.\n\n"
            "Here's what I can help you with:\n"
            "• 🥦 Browse available fruits, vegetables, dairy & more\n"
            "• 🍳 Get recipe ideas from in-stock ingredients\n"
            "• 📦 Track your orders\n"
            "• ⭐ Learn about loyalty points & rewards\n"
            "• 💰 Find budget-friendly options\n\n"
            "Try asking: *\"What fruits do you have?\"* or *\"Suggest a vegetable recipe\"*"
        )

    # ── VEGETABLES ─────────────────────────────────────────────────────────────
    veg_triggers = ['vegetable', 'vegetables', 'veggie', 'veggies', 'sabzi',
                    'sabzis', 'greens', 'vegs', 'what veg']
    if any(w in ml for w in veg_triggers):
        products = get_products_by_category('Vegetable')
        if not products:
            return "😔 We're currently out of vegetables. Please check back soon — we restock daily!"
        
        lines = [f"🥦 **Here are all the vegetables we have in stock right now:**\n"]
        for i, p in enumerate(products, 1):
            desc = f" — {p.description[:50]}..." if p.description and len(p.description) > 10 else ""
            lines.append(f"{i}. **{p.name}** — ₹{p.price:.2f} | ★ {p.average_rating:.1f} | Stock: {p.stock}{desc}")
        
        lines.append(
            f"\n📊 **Total: {len(products)} vegetables available**"
            "\n\n**How to order:**"
            "\n1. Go to the homepage and search for the vegetable name"
            "\n2. Click **Add to Cart** 🛒 on the product card"
            "\n3. Go to **Cart** → **Checkout** to complete your order"
            "\n\n💡 **Tip:** Use the **Category → Vegetable** filter on the homepage to see all at once. "
            "You can also sort by **Price: Low to High** to find the best deals!"
        )
        return "\n".join(lines)

    # ── FRUITS ─────────────────────────────────────────────────────────────────
    fruit_triggers = ['fruit', 'fruits', 'fresh fruit', 'what fruit']
    if any(w in ml for w in fruit_triggers):
        products = get_products_by_category('Fruit')
        if not products:
            return "😔 We're out of fruits right now. Please check back soon — we restock daily!"
        
        lines = [f"🍎 **Here are all the fruits available in FreshMarket right now:**\n"]
        for i, p in enumerate(products, 1):
            desc = f" — {p.description[:50]}..." if p.description and len(p.description) > 10 else ""
            lines.append(f"{i}. **{p.name}** — ₹{p.price:.2f} | ★ {p.average_rating:.1f} | Stock: {p.stock}{desc}")
        
        lines.append(
            f"\n📊 **Total: {len(products)} fruits available**"
            "\n\n**How to order:**"
            "\n1. Search the fruit name in the search bar on the homepage"
            "\n2. Click **Add to Cart** 🛒"
            "\n3. Head to **Cart** → **Checkout** when ready"
            "\n\n💡 **Tip:** Fruits are great for smoothies! Ask me *\"Suggest a fruit smoothie recipe\"* 🥤"
        )
        return "\n".join(lines)

    # ── DAIRY ──────────────────────────────────────────────────────────────────
    dairy_triggers = ['dairy', 'milk', 'cheese', 'butter', 'paneer', 'curd', 'yogurt',
                      'ghee', 'cream', 'dahi']
    if any(w in ml for w in dairy_triggers):
        products = get_products_by_category('Dairy')
        if not products:
            return "😔 We're currently out of dairy products. Please check back soon!"
        
        lines = [f"🥛 **Here are all dairy products available in FreshMarket:**\n"]
        for i, p in enumerate(products, 1):
            desc = f" — {p.description[:50]}..." if p.description and len(p.description) > 10 else ""
            lines.append(f"{i}. **{p.name}** — ₹{p.price:.2f} | ★ {p.average_rating:.1f} | Stock: {p.stock}{desc}")
        
        lines.append(
            f"\n📊 **Total: {len(products)} dairy items available**"
            "\n\n**How to order:**"
            "\n1. Use the **Category → Dairy** filter on the homepage"
            "\n2. Click **Add to Cart** 🛒 on any item"
            "\n3. Proceed to **Checkout** to place your order"
            "\n\n💡 **Tip:** Dairy products have limited shelf life — order fresh and store properly! ❄️"
        )
        return "\n".join(lines)

    # ── BAKERY ─────────────────────────────────────────────────────────────────
    bakery_triggers = ['bakery', 'bread', 'bun', 'cake', 'biscuit', 'roti', 'atta',
                       'flour', 'toast', 'croissant', 'muffin', 'pastry']
    if any(w in ml for w in bakery_triggers):
        products = get_products_by_category('Bakery')
        if not products:
            return "😔 We're currently out of bakery products. Please check back soon!"
        
        lines = [f"🍞 **Here are all bakery products available in FreshMarket:**\n"]
        for i, p in enumerate(products, 1):
            lines.append(f"{i}. **{p.name}** — ₹{p.price:.2f} | ★ {p.average_rating:.1f} | Stock: {p.stock}")
        
        lines.append(
            f"\n📊 **Total: {len(products)} bakery items available**"
            "\n\n**How to order:**"
            "\n1. Search the item name in the homepage search bar"
            "\n2. Click **Add to Cart** 🛒"
            "\n3. Proceed to **Checkout** when done shopping"
            "\n\n💡 **Tip:** Bakery items are best when fresh! Order frequently for the freshest bakes. 🥐"
        )
        return "\n".join(lines)

    # ── ALL ITEMS / EVERYTHING ─────────────────────────────────────────────────
    all_triggers = ['all items', 'all products', 'everything', 'full list', 'complete list',
                    'what do you have', 'what do you sell', 'what products', 'your stock',
                    'show me all', 'list everything', 'catalog', 'catalogue']
    if any(w in ml for w in all_triggers):
        products = get_all_in_stock()
        if not products:
            return "😔 No products are in stock right now. Please check back soon!"
        
        categories = {}
        for p in products:
            categories.setdefault(p.category, []).append(p)
        
        lines = [f"🛒 **FreshMarket Full Product Catalog ({len(products)} items in stock):**\n"]
        cat_emojis = {
            'Vegetable': '🥦', 'Fruit': '🍎', 'Dairy': '🥛', 'Bakery': '🍞',
            'Grain': '🌾', 'Meat': '🍗', 'Seafood': '🐟', 'Beverage': '🧃',
            'Snack': '🍿', 'Spice': '🌶️', 'Oil': '🫙', 'Frozen': '❄️'
        }
        for cat, items in sorted(categories.items()):
            emoji = cat_emojis.get(cat, '📦')
            lines.append(f"\n{emoji} **{cat}** ({len(items)} items)")
            for p in items[:8]:  # Show top 8 per category
                lines.append(f"  • {p.name} — ₹{p.price:.2f} ★{p.average_rating:.1f}")
            if len(items) > 8:
                lines.append(f"  _...and {len(items) - 8} more_")
        
        lines.append(
            "\n\n**How to shop:**"
            "\n1. Browse by category using the filter on the homepage"
            "\n2. Search any product by name in the search bar"
            "\n3. Click **Add to Cart** 🛒 to add items"
            "\n4. Apply coupons at checkout for discounts!"
            "\n\n💡 Ask me about a specific category for a full list with prices!"
        )
        return "\n".join(lines)

    # ── SPECIFIC PRODUCT SEARCH ────────────────────────────────────────────────
    search_triggers = ['do you have', 'is there', 'looking for', 'find me', 'search for',
                       'any stock of', 'stock of', 'price of']
    if any(w in ml for w in search_triggers):
        try:
            # Try to find a matching product
            from models import Product
            from sqlalchemy import or_
            words = [w for w in ml.split() if len(w) > 3
                     and w not in ('have', 'there', 'find', 'search', 'looking', 'price', 'stock')]
            
            if words:
                query = Product.query.filter(Product.stock > 0)
                query = query.filter(or_(*[Product.name.ilike(f'%{w}%') for w in words]))
                found = query.order_by(Product.average_rating.desc()).limit(8).all()
                
                if found:
                    lines = [f"🔍 **Found {len(found)} matching product(s):**\n"]
                    for i, p in enumerate(found, 1):
                        desc = f"\n   _{p.description[:80]}_" if p.description else ""
                        lines.append(f"{i}. **{p.name}** — ₹{p.price:.2f} | ★ {p.average_rating:.1f} | Stock: {p.stock}{desc}")
                    lines.append(
                        "\n\n**To add to cart:** Click the 🛒 **Add to Cart** button on the product card on the homepage."
                    )
                    return "\n".join(lines)
                else:
                    return (
                        f"😔 Sorry, I couldn't find that product in our current stock. "
                        "Try browsing the homepage using **Search** or **Category filters** — "
                        "we might have something similar! Or ask me about a specific category like *\"Show me all vegetables\"*."
                    )
        except Exception:
            pass

    # ── RECIPES ────────────────────────────────────────────────────────────────
    recipe_triggers = ['recipe', 'recipes', 'cook', 'cooking', 'make', 'prepare', 'dish',
                       'meal', 'food idea', 'what to cook', 'dinner', 'lunch', 'breakfast']
    if any(w in ml for w in recipe_triggers):
        veggies = get_products_by_category('Vegetable')[:5]
        fruits  = get_products_by_category('Fruit')[:3]
        dairy   = get_products_by_category('Dairy')[:3]

        # Detect specific recipe type
        if 'smoothie' in ml or 'juice' in ml:
            if fruits:
                names = [p.name for p in fruits]
                return (
                    f"🥤 **Fruit Smoothie Recipe** using FreshMarket ingredients:\n\n"
                    f"**Ingredients available in our store:**\n"
                    + "\n".join([f"• {p.name} — ₹{p.price:.2f}" for p in fruits]) +
                    "\n\n**Instructions:**\n"
                    "1. Wash and peel your fruits\n"
                    "2. Chop into small pieces\n"
                    "3. Add fruits + 1 cup milk/yogurt to a blender\n"
                    "4. Blend on high for 60 seconds\n"
                    "5. Add honey to taste, pour over ice and enjoy! 🍹\n\n"
                    "💡 Add all these to cart by searching each name on the homepage!"
                )

        if 'salad' in ml:
            if veggies:
                return (
                    f"🥗 **Fresh Vegetable Salad Recipe:**\n\n"
                    f"**Available ingredients in our store:**\n"
                    + "\n".join([f"• {p.name} — ₹{p.price:.2f}" for p in veggies[:5]]) +
                    "\n\n**Instructions:**\n"
                    "1. Wash all vegetables thoroughly\n"
                    "2. Chop tomatoes, cucumbers, and onions into cubes\n"
                    "3. Mix together in a bowl\n"
                    "4. Drizzle with olive oil, lemon juice, salt & pepper\n"
                    "5. Toss well and serve fresh! 🫒\n\n"
                    "**To order these ingredients:**\n"
                    "1. Search each vegetable name on the homepage\n"
                    "2. Add to cart 🛒\n"
                    "3. Checkout and get them delivered!"
                )

        # Generic recipe suggestion
        if veggies and dairy:
            veg_list = "\n".join([f"• {p.name} — ₹{p.price:.2f}" for p in veggies[:4]])
            dairy_list = "\n".join([f"• {p.name} — ₹{p.price:.2f}" for p in dairy[:2]])
            return (
                f"🍳 **Quick Vegetable Sabzi Recipe** using ingredients from FreshMarket:\n\n"
                f"**Vegetables you'll need (available now):**\n{veg_list}\n\n"
                f"**Dairy/extras (available now):**\n{dairy_list}\n\n"
                f"**Instructions:**\n"
                "1. Heat 2 tbsp oil in a pan on medium flame\n"
                "2. Add cumin seeds and let them splutter\n"
                "3. Add chopped onion and cook until golden\n"
                "4. Add ginger-garlic paste, stir for 1 minute\n"
                "5. Add chopped vegetables, salt, turmeric, red chilli powder\n"
                "6. Cover and cook for 10-12 minutes until tender\n"
                "7. Finish with garam masala and fresh coriander. Serve with roti! 🫓\n\n"
                "**How to order these items:**\n"
                "1. Search each ingredient on the homepage\n"
                "2. Click **Add to Cart** 🛒\n"
                "3. Go to Cart → Checkout\n\n"
                "💡 Want a specific recipe? Ask me like *\"Recipe using tomato and potato\"*!"
            )

    # ── PRICE / BUDGET ─────────────────────────────────────────────────────────
    budget_triggers = ['cheap', 'budget', 'affordable', 'cheapest', 'lowest price',
                       'best deal', 'most affordable', 'under ₹', 'under rs']
    if any(w in ml for w in budget_triggers):
        try:
            cheap = (Product.query.filter(Product.stock > 0)
                     .order_by(Product.price.asc()).limit(8).all())
            if cheap:
                lines = ["💰 **Most affordable items right now:**\n"]
                for i, p in enumerate(cheap, 1):
                    lines.append(f"{i}. **{p.name}** ({p.category}) — ₹{p.price:.2f} | ★ {p.average_rating:.1f}")
                lines.append(
                    "\n\n💡 **Save more with:**"
                    "\n• **Loyalty Points** — earn 1 point per ₹10 spent, redeem for discounts"
                    "\n• **Coupon codes** — apply at checkout for extra savings"
                    "\n• **Price filter** — use the slider on the homepage to set your budget"
                )
                return "\n".join(lines)
        except Exception:
            pass
        return "💰 Use the price range filter on the homepage to find products within your budget. Also earn loyalty points on every order to get future discounts!"

    # ── ORDER TRACKING ─────────────────────────────────────────────────────────
    order_triggers = ['order', 'my order', 'track', 'tracking', 'delivery', 'status',
                      'where is', 'dispatched', 'shipped', 'when will']
    if any(w in ml for w in order_triggers):
        if user and user.is_authenticated:
            orders = get_user_order_context(user.id)
            if orders:
                lines = [f"📦 **Your Recent Orders, {user.username}:**\n"]
                for o in orders:
                    status_emoji = {'Completed': '✅', 'Pending': '⏳', 'Processing': '🔄',
                                    'Cancelled': '❌', 'Shipped': '🚚'}.get(o['status'], '📦')
                    lines.append(f"**Order #{o['order_id']}** — {o['date']}")
                    lines.append(f"  Status: {status_emoji} {o['status']}")
                    lines.append(f"  Items: {', '.join(o['items'][:4])}")
                    lines.append(f"  Total: {o['total']}\n")
                lines.append(
                    "**For full order details:**\n"
                    "1. Go to your **Profile** in the navbar\n"
                    "2. Click **Orders** to see all orders\n"
                    "3. Click on an order to see complete item-by-item breakdown"
                )
                return "\n".join(lines)
            else:
                return (
                    "📦 You don't have any orders yet! Start shopping and your order history will appear here.\n\n"
                    "**To place your first order:**\n"
                    "1. Browse products on the homepage\n"
                    "2. Add items to your cart 🛒\n"
                    "3. Go to Checkout → Choose payment → Confirm!"
                )
        return (
            "📦 To track your orders, please **log in** first, then go to your **Profile → Orders**.\n\n"
            "**Steps:**\n"
            "1. Click **Login** in the navbar\n"
            "2. Enter your credentials\n"
            "3. Click **Profile** → **Orders** to see all your orders"
        )

    # ── CART ───────────────────────────────────────────────────────────────────
    cart_triggers = ['cart', 'basket', 'buy', 'purchase', 'checkout', 'add to cart',
                     'how to buy', 'how to add', 'how to order']
    if any(w in ml for w in cart_triggers):
        return (
            "🛒 **How to shop on FreshMarket:**\n\n"
            "**Step 1 — Find your products:**\n"
            "• Use the **search bar** at the top to search by name\n"
            "• Use **Category filter** to browse Vegetables, Fruits, Dairy, etc.\n"
            "• Use **Sort by** to sort by price or rating\n\n"
            "**Step 2 — Add to Cart:**\n"
            "• Click the **🛒 Add to Cart** button on any product card\n"
            "• Use **+** / **-** buttons to adjust quantity\n"
            "• Click the ❤️ icon to add to Wishlist for later\n\n"
            "**Step 3 — Checkout:**\n"
            "• Click the **🛒 Cart** icon in the navbar\n"
            "• Review your items and total\n"
            "• Apply a **coupon code** for discount\n"
            "• Redeem **loyalty points** if you have any\n"
            "• Choose **payment method** (COD, Card, UPI)\n"
            "• Click **Place Order** — done! ✅"
        )

    # ── LOYALTY POINTS ─────────────────────────────────────────────────────────
    loyalty_triggers = ['loyalty', 'points', 'rewards', 'redeem', 'earn', 'reward program']
    if any(w in ml for w in loyalty_triggers):
        return (
            "⭐ **FreshMarket Loyalty Rewards Program:**\n\n"
            "**How to EARN points:**\n"
            "• Earn **1 point for every ₹10** you spend\n"
            "• Points are automatically added after each order\n"
            "• Example: A ₹500 order earns you 50 points!\n\n"
            "**How to REDEEM points:**\n"
            "• 100 points = ₹10 discount on your next order\n"
            "• Redeem at checkout — just enter the amount to redeem\n"
            "• Minimum redemption: 100 points\n\n"
            "**View your points:**\n"
            "1. Click the ⭐ **Rewards** link in the navbar\n"
            "2. See your current balance & full transaction history\n\n"
            "💡 **Pro Tip:** Stack loyalty points with coupon codes for maximum savings!"
        )

    # ── HELP / CAPABILITIES ────────────────────────────────────────────────────
    help_triggers = ['help', 'what can you', 'capabilities', 'what do you do',
                     'how can you help', 'features', 'options', 'menu']
    if any(w in ml for w in help_triggers):
        return (
            "🤖 **I'm FreshBot — here's everything I can help with:**\n\n"
            "• 🥦 **\"What vegetables do you have?\"** — Full list with prices\n"
            "• 🍎 **\"Show me all fruits\"** — Fruits catalog with ratings\n"
            "• 🥛 **\"What dairy products are available?\"** — Dairy listing\n"
            "• 🍞 **\"What bakery items do you have?\"** — Bakery catalog\n"
            "• 🛒 **\"Show me all products\"** — Complete store catalog\n"
            "• 🍳 **\"Suggest a recipe\"** — Recipes using in-stock ingredients\n"
            "• 💰 **\"Show cheapest items\"** — Budget-friendly options\n"
            "• 📦 **\"Where is my order?\"** — Your order status & history\n"
            "• ⭐ **\"How do loyalty points work?\"** — Rewards explanation\n"
            "• 🛒 **\"How do I add to cart?\"** — Step-by-step shopping guide\n\n"
            "Just type your question naturally and I'll help! 😊"
        )

    # ── NUTRITION / HEALTHY ────────────────────────────────────────────────────
    health_triggers = ['healthy', 'nutrition', 'diet', 'vitamin', 'protein', 'calcium',
                       'iron', 'fiber', 'calories', 'organic', 'weight loss']
    if any(w in ml for w in health_triggers):
        veggies = get_products_by_category('Vegetable')[:4]
        fruits  = get_products_by_category('Fruit')[:4]
        veg_names  = ", ".join([p.name for p in veggies])  if veggies  else "various vegetables"
        fruit_names= ", ".join([p.name for p in fruits])   if fruits   else "various fruits"
        return (
            f"🥗 **Healthy Eating Guide from FreshMarket:**\n\n"
            f"**Top vegetables we have ({veg_names}):**\n"
            "• Rich in fiber, vitamins A, C, K\n"
            "• Low in calories, great for weight management\n"
            "• Eat 3–5 servings daily for best health\n\n"
            f"**Fresh fruits available ({fruit_names}):**\n"
            "• Natural sugars + vitamins + antioxidants\n"
            "• Great for immunity and skin health\n"
            "• Eat 2–3 servings of fruit daily\n\n"
            "**Tips for healthy grocery shopping:**\n"
            "1. Fill half your cart with fruits & vegetables\n"
            "2. Choose high-rated products (★ 4+) for best quality\n"
            "3. Use **Sort by Rating** on the homepage to find top picks\n"
            "4. Fresh produce is restocked daily — shop early for best selection!\n\n"
            "💡 Ask me *\"Suggest a healthy recipe\"* or *\"Show me all vegetables\"*!"
        )

    # ── PAYMENT ────────────────────────────────────────────────────────────────
    payment_triggers = ['payment', 'pay', 'upi', 'card', 'cod', 'cash', 'online payment',
                        'debit', 'credit', 'gpay', 'phonepe', 'razorpay']
    if any(w in ml for w in payment_triggers):
        return (
            "💳 **Payment Options at FreshMarket:**\n\n"
            "We accept all major payment methods:\n\n"
            "• 💵 **Cash on Delivery (COD)** — Pay when your order arrives\n"
            "• 💳 **Debit Card** — All major banks supported\n"
            "• 💳 **Credit Card** — Visa, Mastercard, etc.\n"
            "• 📱 **UPI** — GooglePay, PhonePe, Paytm, BHIM & more\n\n"
            "**At checkout you can also:**\n"
            "• Apply **coupon codes** for discounts\n"
            "• Redeem **loyalty points** (100 pts = ₹10 off)\n"
            "• Schedule delivery for a specific date & time\n\n"
            "All payments are 100% secure! 🔒"
        )

    # ── DEFAULT RESPONSE ───────────────────────────────────────────────────────
    return (
        "🤖 Hi! I'm **FreshBot**, your FreshMarket shopping assistant!\n\n"
        "Here are some things you can ask me:\n"
        "• *\"What vegetables do you have?\"*\n"
        "• *\"Show me all fruits\"*\n"
        "• *\"Suggest a recipe for dinner\"*\n"
        "• *\"Where is my order?\"*\n"
        "• *\"Show cheapest items\"*\n"
        "• *\"How do loyalty points work?\"*\n\n"
        "What can I help you with today? 😊"
    )

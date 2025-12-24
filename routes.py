from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import secrets
import json
from datetime import datetime, timedelta
from extensions import db, login_manager, oauth
from models import User, Product, CartItem, Order, OrderItem, Address, Wishlist, Review, Coupon, LoyaltyTransaction, ScheduledOrder

from sqlalchemy import or_

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Home & Products ---
@main.route('/')
def index():
    # Get filter parameters
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '')
    sort_by = request.args.get('sort', 'name_asc')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    min_rating = request.args.get('min_rating', type=float)
    in_stock_only = request.args.get('in_stock') == '1'
    
    # Base query
    query = Product.query
    
    # Apply search filter
    if search_query:
        query = query.filter(or_(
            Product.name.ilike(f'%{search_query}%'),
            Product.category.ilike(f'%{search_query}%'),
            Product.description.ilike(f'%{search_query}%')
        ))
    
    # Apply category filter
    if category_filter:
        query = query.filter(Product.category == category_filter)
    
    # Apply price range filter
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    
    # Apply stock and rating filters
    if in_stock_only:
        query = query.filter(Product.stock > 0)
    if min_rating is not None and min_rating > 0:
        query = query.filter(Product.average_rating >= min_rating)
    
    # Apply sorting
    if sort_by == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'name_desc':
        query = query.order_by(Product.name.desc())
    elif sort_by == 'rating':
        query = query.order_by(Product.average_rating.desc())
    else:  # name_asc
        query = query.order_by(Product.name.asc())
    
    products = query.all()
    price_bounds = db.session.query(db.func.min(Product.price), db.func.max(Product.price)).first()
    price_floor = round(price_bounds[0], 2) if price_bounds and price_bounds[0] is not None else 0
    price_ceiling = round(price_bounds[1], 2) if price_bounds and price_bounds[1] is not None else 0
    
    # Get all categories for filter
    categories = db.session.query(Product.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    # Build spotlight products (prioritize top-rated, then fresh stock)
    spotlight_products = Product.query.filter(
        Product.stock > 0,
        Product.review_count > 0
    ).order_by(
        Product.average_rating.desc(),
        Product.review_count.desc(),
        Product.price.asc()
    ).limit(3).all()

    if len(spotlight_products) < 3:
        exclude_ids = [product.id for product in spotlight_products]
        fallback_query = Product.query.filter(Product.stock > 0)
        if exclude_ids:
            fallback_query = fallback_query.filter(~Product.id.in_(exclude_ids))
        fallback_products = fallback_query.order_by(
            Product.category.asc(),
            Product.name.asc()
        ).limit(3 - len(spotlight_products)).all()
        spotlight_products.extend(fallback_products)

    # Get cart, wishlist, and reorder data
    cart_quantities = {}
    wishlist_ids = set()
    quick_reorder_items = []
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        cart_quantities = {item.product_id: item.quantity for item in cart_items}
        
        wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
        wishlist_ids = {item.product_id for item in wishlist_items}
        
        recent_items = (
            OrderItem.query.join(Order)
            .filter(Order.user_id == current_user.id)
            .order_by(Order.date.desc(), OrderItem.id.desc())
            .limit(50)
            .all()
        )
        
        reorder_stats = {}
        for item in recent_items:
            if not item.product or item.product.stock <= 0:
                continue
            pid = item.product_id
            order_date = item.order.date if item.order else None
            stats = reorder_stats.get(pid)
            if not stats:
                stats = {
                    'product': item.product,
                    'last_ordered': order_date,
                    'times_ordered': item.quantity
                }
                reorder_stats[pid] = stats
            else:
                stats['times_ordered'] += item.quantity
                if order_date and stats['last_ordered'] and order_date > stats['last_ordered']:
                    stats['last_ordered'] = order_date
                elif order_date and not stats['last_ordered']:
                    stats['last_ordered'] = order_date
        
        quick_reorder_items = sorted(
            reorder_stats.values(),
            key=lambda data: data['last_ordered'] or datetime.min,
            reverse=True
        )[:4]

    # Fresh drop radar (newest arrivals)
    fresh_products = Product.query.order_by(Product.id.desc()).limit(4).all()
    
    return render_template('index.html', 
                         products=products, 
                         cart_quantities=cart_quantities,
                         wishlist_ids=wishlist_ids,
                         categories=categories,
                         current_category=category_filter,
                         current_sort=sort_by,
                         search_query=search_query,
                         min_price=min_price,
                         max_price=max_price,
                         min_rating=min_rating,
                         in_stock_only=in_stock_only,
                         price_floor=price_floor,
                         price_ceiling=price_ceiling,
                         spotlight_products=spotlight_products,
                         quick_reorder_items=quick_reorder_items,
                         fresh_products=fresh_products)

# --- Authentication ---
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid username or password')
    return render_template('login.html', google_login_enabled=current_app.config.get('GOOGLE_LOGIN_ENABLED', False))


@main.route('/login/google')
def google_login():
    if not current_app.config.get('GOOGLE_LOGIN_ENABLED'):
        flash('Google login is not configured. Please use email and password.')
        return redirect(url_for('main.login'))
    redirect_uri = url_for('main.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@main.route('/login/google/callback')
def google_callback():
    if not current_app.config.get('GOOGLE_LOGIN_ENABLED'):
        flash('Google login is not configured.')
        return redirect(url_for('main.login'))

    try:
        token = oauth.google.authorize_access_token()
    except Exception:
        flash('Unable to authenticate with Google. Please try again.')
        return redirect(url_for('main.login'))

    user_info = token.get('userinfo')
    if not user_info:
        resp = oauth.google.get('userinfo')
        user_info = resp.json() if resp.ok else None

    if not user_info:
        flash('Could not retrieve Google account information.')
        return redirect(url_for('main.login'))

    email = user_info.get('email')
    if not email:
        flash('Google account does not have an email address associated.')
        return redirect(url_for('main.login'))

    user = User.query.filter((User.email == email) | (User.username == email)).first()

    if not user:
        base_username = email.split('@')[0]
        candidate = base_username
        counter = 1
        while User.query.filter_by(username=candidate).first():
            candidate = f"{base_username}{counter}"
            counter += 1

        user = User(
            username=candidate,
            email=email,
            password_hash=generate_password_hash(secrets.token_urlsafe(16))
        )
        db.session.add(user)
        db.session.commit()

    login_user(user)
    flash('Logged in with Google.')
    return redirect(url_for('main.index'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('Username or Email already exists')
            return redirect(url_for('main.register'))
            
        new_user = User(username=username, email=email, password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('main.index'))
    return render_template('register.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            token = secrets.token_urlsafe(32)
            user.reset_token = token
            user.reset_token_expiration = datetime.utcnow() + timedelta(hours=1)
            db.session.commit()
            
            # Simulate sending email
            reset_url = url_for('main.reset_password', token=token, _external=True)
            print(f"RESET LINK: {reset_url}")
            flash(f'Reset link sent to console (Dev Mode): {reset_url}')
        else:
            flash('Email not found')
            
        return redirect(url_for('main.login'))
        
    return render_template('forgot_password.html')

@main.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()
    
    if not user or user.reset_token_expiration < datetime.utcnow():
        flash('Invalid or expired token')
        return redirect(url_for('main.login'))
        
    if request.method == 'POST':
        password = request.form.get('password')
        user.password_hash = generate_password_hash(password)
        user.reset_token = None
        user.reset_token_expiration = None
        db.session.commit()
        
        flash('Password reset successfully')
        return redirect(url_for('main.login'))
        
    return render_template('reset_password.html')

# --- Cart & Shop ---
@main.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    
    if product.stock <= 0:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': 'Product is out of stock'})
        flash('Product is out of stock')
        return redirect(url_for('main.index'))

    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        if cart_item.quantity + 1 > product.stock:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': f'Only {product.stock} items available'})
            flash(f'Only {product.stock} items available')
            return redirect(url_for('main.cart'))
        cart_item.quantity += 1
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)
    db.session.commit()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        total_items = sum(item.quantity for item in cart_items)
        cart_total = sum(item.product.price * item.quantity for item in cart_items)
        return jsonify({
            'success': True, 
            'message': 'Item added to cart', 
            'cart_count': total_items,
            'cart_total': cart_total,
            'item_quantity': cart_item.quantity,
            'product_id': product_id
        })
        
    flash('Item added to cart')
    return redirect(url_for('main.cart'))

@main.route('/decrease_quantity/<int:item_id>')
@login_required
def decrease_quantity(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id == current_user.id:
        if item.quantity > 1:
            item.quantity -= 1
            db.session.commit()
        else:
            db.session.delete(item)
            db.session.commit()
    return redirect(url_for('main.cart'))

@main.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@main.route('/remove_from_cart/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id == current_user.id:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('main.cart'))

# --- Product Details ---
@main.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    reviews = Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).all()
    
    # Get related products (same category, different product)
    related_products = Product.query.filter(
        Product.category == product.category,
        Product.id != product_id
    ).limit(4).all()
    
    # Check if in wishlist
    in_wishlist = False
    if current_user.is_authenticated:
        in_wishlist = Wishlist.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first() is not None
    
    return render_template('product_detail.html', 
                         product=product, 
                         reviews=reviews,
                         related_products=related_products,
                         in_wishlist=in_wishlist)

# --- Wishlist ---
@main.route('/wishlist')
@login_required
def wishlist():
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).order_by(Wishlist.created_at.desc()).all()
    return render_template('wishlist.html', wishlist_items=wishlist_items)

@main.route('/wishlist/add/<int:product_id>')
@login_required
def add_to_wishlist(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Check if already in wishlist
    existing = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if not existing:
        wishlist_item = Wishlist(user_id=current_user.id, product_id=product_id)
        db.session.add(wishlist_item)
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': 'Added to wishlist', 'in_wishlist': True})
        flash('Added to wishlist!')
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': 'Already in wishlist', 'in_wishlist': True})
        flash('Already in wishlist')
    
    return redirect(request.referrer or url_for('main.index'))

@main.route('/wishlist/remove/<int:product_id>')
@login_required
def remove_from_wishlist(product_id):
    wishlist_item = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if wishlist_item:
        db.session.delete(wishlist_item)
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': 'Removed from wishlist', 'in_wishlist': False})
        flash('Removed from wishlist')
    
    return redirect(request.referrer or url_for('main.wishlist'))

@main.route('/wishlist/toggle/<int:product_id>')
@login_required
def toggle_wishlist(product_id):
    """Toggle wishlist status - add if not present, remove if present"""
    product = Product.query.get_or_404(product_id)
    wishlist_item = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if wishlist_item:
        db.session.delete(wishlist_item)
        db.session.commit()
        in_wishlist = False
        message = 'Removed from wishlist'
    else:
        wishlist_item = Wishlist(user_id=current_user.id, product_id=product_id)
        db.session.add(wishlist_item)
        db.session.commit()
        in_wishlist = True
        message = 'Added to wishlist'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'message': message, 'in_wishlist': in_wishlist})
    
    flash(message)
    return redirect(request.referrer or url_for('main.index'))

# --- Reviews ---
@main.route('/product/<int:product_id>/review', methods=['POST'])
@login_required
def add_review(product_id):
    product = Product.query.get_or_404(product_id)
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment', '').strip()
    
    if not rating or rating < 1 or rating > 5:
        flash('Please provide a valid rating (1-5 stars)')
        return redirect(url_for('main.product_detail', product_id=product_id))
    
    # Check if user already reviewed this product
    existing_review = Review.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if existing_review:
        # Update existing review
        existing_review.rating = rating
        existing_review.comment = comment
        existing_review.created_at = datetime.utcnow()
        flash('Your review has been updated!')
    else:
        # Create new review
        review = Review(
            user_id=current_user.id,
            product_id=product_id,
            rating=rating,
            comment=comment
        )
        db.session.add(review)
        flash('Thank you for your review!')
    
    db.session.commit()
    
    # Update product average rating
    reviews = Review.query.filter_by(product_id=product_id).all()
    if reviews:
        product.average_rating = sum(r.rating for r in reviews) / len(reviews)
        product.review_count = len(reviews)
        db.session.commit()
    
    return redirect(url_for('main.product_detail', product_id=product_id))

# --- Orders & Tracking ---
@main.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.date.desc()).all()
    return render_template('orders.html', orders=user_orders)

@main.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Ensure user owns this order
    if order.user_id != current_user.id:
        flash('Unauthorized access')
        return redirect(url_for('main.orders'))
    
    return render_template('order_detail.html', order=order)

@main.route('/order/success/<int:order_id>')
@login_required
def order_success(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Ensure user owns this order
    if order.user_id != current_user.id:
        flash('Unauthorized access')
        return redirect(url_for('main.orders'))
    
    return render_template('order_success.html', order=order)

# --- User Profile ---
@main.route('/profile')
@login_required
def profile():
    # Get user statistics
    total_orders = Order.query.filter_by(user_id=current_user.id).count()
    total_spent = db.session.query(db.func.sum(Order.total_price)).filter_by(user_id=current_user.id).scalar() or 0
    wishlist_count = Wishlist.query.filter_by(user_id=current_user.id).count()
    
    # Get recent orders
    recent_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.date.desc()).limit(5).all()
    
    return render_template('profile.html',
                         total_orders=total_orders,
                         total_spent=total_spent,
                         wishlist_count=wishlist_count,
                         recent_orders=recent_orders)

@main.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        
        # Check if username/email already taken by another user
        existing = User.query.filter(
            (User.username == username) | (User.email == email),
            User.id != current_user.id
        ).first()
        
        if existing:
            flash('Username or email already taken')
            return redirect(url_for('main.edit_profile'))
        
        current_user.username = username
        current_user.email = email
        
        # Update password if provided
        new_password = request.form.get('new_password')
        if new_password:
            current_user.password_hash = generate_password_hash(new_password)
        
        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('main.profile'))
    
    return render_template('edit_profile.html')

@main.route('/checkout')
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Cart is empty')
        return redirect(url_for('main.index'))
        
    total = sum(item.product.price * item.quantity for item in cart_items)
    min_delivery_date = (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d')
    return render_template('checkout.html', cart_items=cart_items, total=total, min_delivery_date=min_delivery_date)

@main.route('/apply_coupon', methods=['POST'])
@login_required
def apply_coupon():
    code = request.form.get('code')
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        return jsonify({'success': False, 'message': 'Cart is empty'})
        
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    coupon = Coupon.query.filter_by(code=code).first()
    if not coupon:
        return jsonify({'success': False, 'message': 'Invalid coupon code'})
        
    if not coupon.active:
        return jsonify({'success': False, 'message': 'Coupon is inactive'})
        
    if coupon.valid_from and coupon.valid_from > datetime.utcnow():
        return jsonify({'success': False, 'message': 'Coupon is not yet valid'})
        
    if coupon.valid_to and coupon.valid_to < datetime.utcnow():
        return jsonify({'success': False, 'message': 'Coupon has expired'})
        
    if coupon.usage_limit and coupon.used_count >= coupon.usage_limit:
        return jsonify({'success': False, 'message': 'Coupon usage limit reached'})
        
    discount = 0
    if coupon.discount_type == 'percentage':
        discount = total * (coupon.discount_value / 100)
    else:
        discount = coupon.discount_value
        
    # Ensure discount doesn't exceed total
    discount = min(discount, total)
    new_total = total - discount
    
    return jsonify({
        'success': True, 
        'message': 'Coupon applied successfully',
        'discount': discount,
        'new_total': new_total,
        'code': code
    })


@main.route('/process_order', methods=['POST'])
@login_required
def process_order():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Cart is empty')
        return redirect(url_for('main.index'))
    
    payment_method = request.form.get('payment_method')
    if not payment_method:
        flash('Please select a payment method')
        return redirect(url_for('main.checkout'))
        
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    # Handle loyalty points redemption
    points_to_redeem = int(request.form.get('redeem_points', 0))
    points_discount = 0
    
    if points_to_redeem > 0:
        if points_to_redeem > current_user.loyalty_points:
            flash('Insufficient loyalty points')
            return redirect(url_for('main.checkout'))
        
        # 100 points = ₹10 discount
        points_discount = (points_to_redeem / 100) * 10
        points_discount = min(points_discount, total)  # Can't exceed total
        total -= points_discount
    
    # Handle order scheduling
    scheduled_date = request.form.get('scheduled_date')
    delivery_time_slot = request.form.get('delivery_time_slot')
    is_recurring = request.form.get('is_recurring') == 'on'
    recurrence_frequency = request.form.get('recurrence_frequency')
    
    # If UPI is selected, show QR code payment page
    if payment_method == 'UPI':
        return render_template('upi_payment.html', total=total)
    
    # Create order
    new_order = Order(
        user_id=current_user.id, 
        total_price=total, 
        status='Completed',
        payment_method=payment_method,
        points_redeemed=points_to_redeem
    )
    
    # Add scheduling info if provided
    if scheduled_date and delivery_time_slot:
        try:
            new_order.scheduled_delivery_date = datetime.strptime(scheduled_date, '%Y-%m-%d')
            new_order.delivery_time_slot = delivery_time_slot
        except ValueError:
            flash('Invalid delivery date format')
            return redirect(url_for('main.checkout'))
    
    db.session.add(new_order)
    db.session.commit()
    
    # Move items to OrderItem and decrement stock
    for item in cart_items:
        if item.quantity > item.product.stock:
            flash(f'Sorry, {item.product.name} is out of stock or requested quantity not available.')
            db.session.delete(new_order)
            db.session.commit()
            return redirect(url_for('main.cart'))

        item.product.stock -= item.quantity
        
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_purchase=item.product.price
        )
        db.session.add(order_item)
        db.session.delete(item)
    
    # Calculate and award loyalty points (1 point per ₹10 spent)
    points_earned = int(total / 10)
    new_order.points_earned = points_earned
    current_user.loyalty_points += points_earned
    
    # Deduct redeemed points
    if points_to_redeem > 0:
        current_user.loyalty_points -= points_to_redeem
        
        # Create redemption transaction
        redemption_transaction = LoyaltyTransaction(
            user_id=current_user.id,
            order_id=new_order.id,
            points=-points_to_redeem,
            transaction_type='redeemed',
            description=f'Redeemed {points_to_redeem} points for ₹{points_discount:.2f} discount'
        )
        db.session.add(redemption_transaction)
    
    # Create earning transaction
    if points_earned > 0:
        earning_transaction = LoyaltyTransaction(
            user_id=current_user.id,
            order_id=new_order.id,
            points=points_earned,
            transaction_type='earned',
            description=f'Earned from order #{new_order.id}'
        )
        db.session.add(earning_transaction)
    
    # Handle recurring orders
    if is_recurring and scheduled_date and delivery_time_slot and recurrence_frequency:
        cart_data = []
        for item in CartItem.query.filter_by(user_id=current_user.id).all():
            cart_data.append({
                'product_id': item.product_id,
                'quantity': item.quantity,
                'price': item.product.price
            })
        
        scheduled_order = ScheduledOrder(
            user_id=current_user.id,
            scheduled_date=datetime.strptime(scheduled_date, '%Y-%m-%d'),
            delivery_time_slot=delivery_time_slot,
            is_recurring=True,
            recurrence_frequency=recurrence_frequency,
            items_json=json.dumps(cart_data),
            total_price=total,
            payment_method=payment_method
        )
        
        # Calculate next delivery date
        if recurrence_frequency == 'daily':
            scheduled_order.next_delivery_date = scheduled_order.scheduled_date + timedelta(days=1)
        elif recurrence_frequency == 'weekly':
            scheduled_order.next_delivery_date = scheduled_order.scheduled_date + timedelta(weeks=1)
        elif recurrence_frequency == 'monthly':
            scheduled_order.next_delivery_date = scheduled_order.scheduled_date + timedelta(days=30)
        
        db.session.add(scheduled_order)
        
    db.session.commit()
    
    # Redirect to success page with order details
    return redirect(url_for('main.order_success', order_id=new_order.id))

@main.route('/confirm_payment', methods=['POST'])
@login_required
def confirm_payment():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Cart is empty')
        return redirect(url_for('main.index'))
    
    payment_method = request.form.get('payment_method')
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    # Create Order
    new_order = Order(
        user_id=current_user.id, 
        total_price=total, 
        status='Completed',
        payment_method=payment_method
    )
    db.session.add(new_order)
    db.session.commit() # Commit to get ID
    
    # Move items to OrderItem and decrement stock
    for item in cart_items:
        # Check stock again before finalizing
        if item.quantity > item.product.stock:
            flash(f'Sorry, {item.product.name} is out of stock or requested quantity not available.')
            db.session.delete(new_order) # Rollback order
            db.session.commit()
            return redirect(url_for('main.cart'))

        item.product.stock -= item.quantity # Decrement stock

        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_purchase=item.product.price
        )
        db.session.add(order_item)
        db.session.delete(item) # Clear cart
        
    db.session.commit()
    return redirect(url_for('main.order_success', order_id=new_order.id))

# --- Address Management ---
@main.route('/addresses')
@login_required
def addresses():
    user_addresses = Address.query.filter_by(user_id=current_user.id).order_by(Address.is_default.desc(), Address.created_at.desc()).all()
    return render_template('addresses.html', addresses=user_addresses)

@main.route('/address/add', methods=['GET', 'POST'])
@login_required
def add_address():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        address_line1 = request.form.get('address_line1')
        address_line2 = request.form.get('address_line2')
        city = request.form.get('city')
        state = request.form.get('state')
        pincode = request.form.get('pincode')
        is_default = request.form.get('is_default') == 'on'
        
        # If setting as default, unset other defaults
        if is_default:
            Address.query.filter_by(user_id=current_user.id, is_default=True).update({'is_default': False})
        
        new_address = Address(
            user_id=current_user.id,
            full_name=full_name,
            phone=phone,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            pincode=pincode,
            is_default=is_default
        )
        db.session.add(new_address)
        db.session.commit()
        flash('Address added successfully!')
        return redirect(url_for('main.addresses'))
    
    return render_template('address_form.html', address=None)

@main.route('/address/edit/<int:address_id>', methods=['GET', 'POST'])
@login_required
def edit_address(address_id):
    address = Address.query.get_or_404(address_id)
    
    if address.user_id != current_user.id:
        flash('Unauthorized access')
        return redirect(url_for('main.addresses'))
    
    if request.method == 'POST':
        address.full_name = request.form.get('full_name')
        address.phone = request.form.get('phone')
        address.address_line1 = request.form.get('address_line1')
        address.address_line2 = request.form.get('address_line2')
        address.city = request.form.get('city')
        address.state = request.form.get('state')
        address.pincode = request.form.get('pincode')
        is_default = request.form.get('is_default') == 'on'
        
        # If setting as default, unset other defaults
        if is_default and not address.is_default:
            Address.query.filter_by(user_id=current_user.id, is_default=True).update({'is_default': False})
        
        address.is_default = is_default
        db.session.commit()
        flash('Address updated successfully!')
        return redirect(url_for('main.addresses'))
    
    return render_template('address_form.html', address=address)

@main.route('/address/delete/<int:address_id>', methods=['POST'])
@login_required
def delete_address(address_id):
    address = Address.query.get_or_404(address_id)
    
    if address.user_id != current_user.id:
        flash('Unauthorized access')
        return redirect(url_for('main.addresses'))
    
    db.session.delete(address)
    db.session.commit()
    flash('Address deleted successfully!')
    return redirect(url_for('main.addresses'))

@main.route('/address/set_default/<int:address_id>', methods=['POST'])
@login_required
def set_default_address(address_id):
    address = Address.query.get_or_404(address_id)
    
    if address.user_id != current_user.id:
        flash('Unauthorized access')
        return redirect(url_for('main.addresses'))
    
    # Unset all defaults for this user
    Address.query.filter_by(user_id=current_user.id, is_default=True).update({'is_default': False})
    
    # Set this address as default
    address.is_default = True
    db.session.commit()
    flash('Default address updated!')
    return redirect(url_for('main.addresses'))

# --- Admin ---
@main.route('/admin/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_admin:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        category = request.form.get('category')
        stock = int(request.form.get('stock'))
        
        image = request.files.get('image')
        image_url = None
        
        if image and image.filename:
            filename = secure_filename(image.filename)
            image_path = os.path.join('static', 'images', filename)
            # Ensure directory exists
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image.save(image_path)
            image_url = f'images/{filename}'
        
        new_product = Product(name=name, price=price, category=category, stock=stock, image_url=image_url)
        db.session.add(new_product)
        db.session.commit()
        flash('Product added')
        return redirect(url_for('main.index'))
        
    return render_template('add_product.html')

@main.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('main.index'))
        
    orders = Order.query.order_by(Order.date.desc()).all()
    products = Product.query.order_by(Product.name).all()
    return render_template('admin_dashboard.html', orders=orders, products=products)

@main.route('/admin/order/<int:order_id>/update', methods=['POST'])
@login_required
def update_order_status(order_id):
    if not current_user.is_admin:
        return redirect(url_for('main.index'))
        
    order = Order.query.get_or_404(order_id)
    status = request.form.get('status')
    if status:
        order.status = status
        db.session.commit()
        flash(f'Order #{order.id} status updated to {status}')
        
    return redirect(url_for('main.admin_dashboard'))

@main.route('/admin/product/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    if not current_user.is_admin:
        return redirect(url_for('main.index'))
        
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.price = float(request.form.get('price'))
        product.category = request.form.get('category')
        product.stock = int(request.form.get('stock'))
        product.description = request.form.get('description')
        product.detailed_description = request.form.get('detailed_description')
        
        image = request.files.get('image')
        if image and image.filename:
            filename = secure_filename(image.filename)
            image_path = os.path.join('static', 'images', filename)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image.save(image_path)
            product.image_url = f'images/{filename}'
            
        db.session.commit()
        flash('Product updated successfully')
        return redirect(url_for('main.admin_dashboard'))
        
    return render_template('add_product.html', product=product, is_edit=True)

@main.route('/admin/product/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
    if not current_user.is_admin:
        return redirect(url_for('main.index'))
        
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully')
    return redirect(url_for('main.admin_dashboard'))

@main.route('/admin/coupons')
@login_required
def admin_coupons():
    if not current_user.is_admin:
        return redirect(url_for('main.index'))
    coupons = Coupon.query.all()
    return render_template('admin_coupons.html', coupons=coupons)

@main.route('/admin/coupon/add', methods=['POST'])
@login_required
def add_coupon():
    if not current_user.is_admin:
        return redirect(url_for('main.index'))
        
    code = request.form.get('code')
    discount_type = request.form.get('discount_type')
    discount_value = float(request.form.get('discount_value'))
    valid_to_str = request.form.get('valid_to')
    usage_limit = request.form.get('usage_limit')
    
    valid_to = None
    if valid_to_str:
        valid_to = datetime.strptime(valid_to_str, '%Y-%m-%d')
        
    new_coupon = Coupon(
        code=code,
        discount_type=discount_type,
        discount_value=discount_value,
        valid_to=valid_to,
        usage_limit=int(usage_limit) if usage_limit else None
    )
    
    try:
        db.session.add(new_coupon)
        db.session.commit()
        flash('Coupon added successfully')
    except Exception as e:
        flash('Error adding coupon: Code might already exist')
        
    return redirect(url_for('main.admin_coupons'))

@main.route('/admin/coupon/delete/<int:coupon_id>', methods=['POST'])
@login_required
def delete_coupon(coupon_id):
    if not current_user.is_admin:
        return redirect(url_for('main.index'))
        
    coupon = Coupon.query.get_or_404(coupon_id)
    db.session.delete(coupon)
    db.session.commit()
    flash('Coupon deleted')
    return redirect(url_for('main.admin_coupons'))

    coupon = Coupon.query.get_or_404(coupon_id)
    coupon.active = not coupon.active
    db.session.commit()
    return redirect(url_for('main.admin_coupons'))

@main.route('/admin/api/stats')
@login_required
def admin_stats():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
        
    # Daily Sales (Last 7 days)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)
    
    daily_sales = db.session.query(
        db.func.date(Order.date).label('date'),
        db.func.sum(Order.total_price).label('total')
    ).filter(
        Order.date >= start_date,
        Order.status != 'Cancelled'
    ).group_by('date').all()
    
    sales_data = {
        'labels': [day.strftime('%Y-%m-%d') for day in (start_date + timedelta(n) for n in range(8))],
        'values': [0] * 8
    }
    
    # Map query results to dates
    sales_map = {str(r.date): r.total for r in daily_sales}
    for i, date_str in enumerate(sales_data['labels']):
        if date_str in sales_map:
            sales_data['values'][i] = sales_map[date_str]
            
    # Top Products
    top_products = db.session.query(
        Product.name,
        db.func.sum(OrderItem.quantity).label('total_qty')
    ).join(OrderItem).group_by(Product.name).order_by(db.desc('total_qty')).limit(5).all()
    
    product_data = {
        'labels': [p.name for p in top_products],
        'values': [p.total_qty for p in top_products]
    }
    
    # Order Status
    status_counts = db.session.query(
        Order.status,
        db.func.count(Order.id)
    ).group_by(Order.status).all()
    
    status_data = {
        'labels': [s[0] for s in status_counts],
        'values': [s[1] for s in status_counts]
    }
    
    return jsonify({
        'sales': sales_data,
        'products': product_data,
        'status': status_data
    })

@main.context_processor
def inject_cart_total():
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        total_items = sum(item.quantity for item in cart_items)
        return {'cart_total': total_price, 'cart_count': total_items}
    return {'cart_total': 0, 'cart_count': 0}

# --- Loyalty Rewards ---
@main.route('/loyalty')
@login_required
def loyalty():
    """Display loyalty rewards dashboard"""
    transactions = LoyaltyTransaction.query.filter_by(user_id=current_user.id).order_by(LoyaltyTransaction.created_at.desc()).all()
    
    # Calculate points breakdown
    total_earned = sum(t.points for t in transactions if t.transaction_type == 'earned')
    total_redeemed = abs(sum(t.points for t in transactions if t.transaction_type == 'redeemed'))
    
    return render_template('loyalty.html', 
                         transactions=transactions,
                         total_earned=total_earned,
                         total_redeemed=total_redeemed)

@main.route('/redeem_points', methods=['POST'])
@login_required
def redeem_points():
    """Apply loyalty points as discount during checkout"""
    points_to_redeem = int(request.form.get('points', 0))
    
    if points_to_redeem < 50:
        return jsonify({'success': False, 'message': 'Minimum 50 points required for redemption'})
    
    if points_to_redeem > current_user.loyalty_points:
        return jsonify({'success': False, 'message': 'Insufficient points'})
    
    # Calculate discount (100 points = ₹10)
    discount = (points_to_redeem / 100) * 10
    
    return jsonify({
        'success': True,
        'points': points_to_redeem,
        'discount': discount,
        'message': f'{points_to_redeem} points = ₹{discount:.2f} discount'
    })

# --- Scheduled Orders ---
@main.route('/scheduled_orders')
@login_required
def scheduled_orders():
    """Display all scheduled and recurring orders"""
    orders = ScheduledOrder.query.filter_by(user_id=current_user.id, is_active=True).order_by(ScheduledOrder.scheduled_date.asc()).all()
    
    # Parse items JSON for each order
    for order in orders:
        try:
            order.items = json.loads(order.items_json)
        except:
            order.items = []
    
    return render_template('scheduled_orders.html', orders=orders)

@main.route('/schedule_order', methods=['POST'])
@login_required
def schedule_order():
    """Create a new scheduled order"""
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Cart is empty')
        return redirect(url_for('main.index'))
    
    scheduled_date_str = request.form.get('scheduled_date')
    delivery_time_slot = request.form.get('delivery_time_slot')
    is_recurring = request.form.get('is_recurring') == 'on'
    recurrence_frequency = request.form.get('recurrence_frequency')
    payment_method = request.form.get('payment_method')
    
    if not scheduled_date_str or not delivery_time_slot:
        flash('Please select delivery date and time slot')
        return redirect(url_for('main.checkout'))
    
    try:
        scheduled_date = datetime.strptime(scheduled_date_str, '%Y-%m-%d')
        
        # Validate date is in future
        if scheduled_date.date() < datetime.now().date():
            flash('Scheduled date must be in the future')
            return redirect(url_for('main.checkout'))
        
    except ValueError:
        flash('Invalid date format')
        return redirect(url_for('main.checkout'))
    
    # Prepare cart data
    cart_data = []
    total = 0
    for item in cart_items:
        cart_data.append({
            'product_id': item.product_id,
            'product_name': item.product.name,
            'quantity': item.quantity,
            'price': item.product.price
        })
        total += item.product.price * item.quantity
    
    # Create scheduled order
    scheduled_order = ScheduledOrder(
        user_id=current_user.id,
        scheduled_date=scheduled_date,
        delivery_time_slot=delivery_time_slot,
        is_recurring=is_recurring,
        recurrence_frequency=recurrence_frequency if is_recurring else None,
        items_json=json.dumps(cart_data),
        total_price=total,
        payment_method=payment_method
    )
    
    # Calculate next delivery for recurring orders
    if is_recurring and recurrence_frequency:
        if recurrence_frequency == 'daily':
            scheduled_order.next_delivery_date = scheduled_date + timedelta(days=1)
        elif recurrence_frequency == 'weekly':
            scheduled_order.next_delivery_date = scheduled_date + timedelta(weeks=1)
        elif recurrence_frequency == 'monthly':
            scheduled_order.next_delivery_date = scheduled_date + timedelta(days=30)
    
    db.session.add(scheduled_order)
    db.session.commit()
    
    flash(f'Order scheduled for {scheduled_date.strftime("%B %d, %Y")} - {delivery_time_slot}')
    return redirect(url_for('main.scheduled_orders'))

@main.route('/scheduled_order/cancel/<int:order_id>', methods=['POST'])
@login_required
def cancel_scheduled_order(order_id):
    """Cancel a scheduled order"""
    order = ScheduledOrder.query.get_or_404(order_id)
    
    if order.user_id != current_user.id:
        flash('Unauthorized access')
        return redirect(url_for('main.scheduled_orders'))
    
    order.is_active = False
    db.session.commit()
    flash('Scheduled order cancelled')
    return redirect(url_for('main.scheduled_orders'))

@main.route('/scheduled_order/edit/<int:order_id>', methods=['GET', 'POST'])
@login_required
def edit_scheduled_order(order_id):
    """Edit a scheduled order"""
    order = ScheduledOrder.query.get_or_404(order_id)
    
    if order.user_id != current_user.id:
        flash('Unauthorized access')
        return redirect(url_for('main.scheduled_orders'))
    
    if request.method == 'POST':
        scheduled_date_str = request.form.get('scheduled_date')
        delivery_time_slot = request.form.get('delivery_time_slot')
        
        try:
            order.scheduled_date = datetime.strptime(scheduled_date_str, '%Y-%m-%d')
            order.delivery_time_slot = delivery_time_slot
            
            # Update next delivery for recurring orders
            if order.is_recurring and order.recurrence_frequency:
                if order.recurrence_frequency == 'daily':
                    order.next_delivery_date = order.scheduled_date + timedelta(days=1)
                elif order.recurrence_frequency == 'weekly':
                    order.next_delivery_date = order.scheduled_date + timedelta(weeks=1)
                elif order.recurrence_frequency == 'monthly':
                    order.next_delivery_date = order.scheduled_date + timedelta(days=30)
            
            db.session.commit()
            flash('Scheduled order updated')
            return redirect(url_for('main.scheduled_orders'))
        except ValueError:
            flash('Invalid date format')
    
    # Parse items for display
    try:
        order.items = json.loads(order.items_json)
    except:
        order.items = []
    
    return render_template('edit_scheduled_order.html', order=order)

@main.route('/seed')

def seed_database():
    if Product.query.first():
        flash('Database already contains products.')
        return redirect(url_for('main.index'))
        
    # Create Admin User
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin', 
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'), 
            is_admin=True
        )
        db.session.add(admin)
    
    products = [
        Product(name='Apple', category='Fruit', price=1.20, stock=100, image_url='images/apple.png'),
        Product(name='Banana', category='Fruit', price=0.50, stock=150, image_url='images/fruit.png'),
        Product(name='Orange', category='Fruit', price=0.90, stock=120, image_url='images/fruit.png'),
        Product(name='Grapes', category='Fruit', price=2.50, stock=80, image_url='images/fruit.png'),
        Product(name='Milk', category='Dairy', price=3.50, stock=50, image_url='images/dairy.png'),
        Product(name='Yogurt', category='Dairy', price=1.80, stock=60, image_url='images/dairy.png'),
        Product(name='Cheese', category='Dairy', price=4.50, stock=40, image_url='images/dairy.png'),
        Product(name='Bread', category='Bakery', price=2.00, stock=40, image_url='images/bakery.png'),
        Product(name='Croissant', category='Bakery', price=1.50, stock=30, image_url='images/bakery.png'),
        Product(name='Eggs', category='Dairy', price=4.00, stock=60, image_url='images/dairy.png'),
        Product(name='Chicken Breast', category='Meat', price=7.50, stock=30, image_url='images/vegetable.png'),
        Product(name='Ground Beef', category='Meat', price=6.00, stock=25, image_url='images/vegetable.png'),
        Product(name='Rice', category='Grains', price=5.00, stock=80, image_url='images/bakery.png'),
        Product(name='Pasta', category='Grains', price=2.50, stock=70, image_url='images/bakery.png'),
        Product(name='Tomato', category='Vegetable', price=0.80, stock=120, image_url='images/vegetable.png'),
        Product(name='Carrot', category='Vegetable', price=0.60, stock=100, image_url='images/vegetable.png'),
        Product(name='Lettuce', category='Vegetable', price=1.20, stock=50, image_url='images/vegetable.png'),
        Product(name='Potato', category='Vegetable', price=0.40, stock=150, image_url='images/vegetable.png'),
        Product(name='Onion', category='Vegetable', price=0.50, stock=130, image_url='images/vegetable.png'),
        Product(name='Olive Oil', category='Pantry', price=8.00, stock=40, image_url='images/bakery.png'),
    ]
    
    db.session.bulk_save_objects(products)
    db.session.commit()
    flash('Database seeded with admin and sample products!')
    return redirect(url_for('main.index'))

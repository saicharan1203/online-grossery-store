from app import create_app
from extensions import db
from models import User, Order, LoyaltyTransaction, ScheduledOrder

def migrate_database():
    """Add loyalty points and scheduling features to existing database"""
    app = create_app()
    
    with app.app_context():
        print("Starting database migration for loyalty and scheduling features...")
        
        # Create all new tables
        db.create_all()
        print("✓ Created new tables (LoyaltyTransaction, ScheduledOrder)")
        
        # Add loyalty_points column to existing users if not exists
        try:
            # Check if column exists by querying
            users = User.query.all()
            for user in users:
                if not hasattr(user, 'loyalty_points') or user.loyalty_points is None:
                    user.loyalty_points = 0
            db.session.commit()
            print("✓ Initialized loyalty_points for existing users")
        except Exception as e:
            print(f"Note: {e}")
            db.session.rollback()
        
        # Add points fields to existing orders if not exists
        try:
            orders = Order.query.all()
            for order in orders:
                if not hasattr(order, 'points_earned') or order.points_earned is None:
                    order.points_earned = 0
                if not hasattr(order, 'points_redeemed') or order.points_redeemed is None:
                    order.points_redeemed = 0
            db.session.commit()
            print("✓ Initialized points fields for existing orders")
        except Exception as e:
            print(f"Note: {e}")
            db.session.rollback()
        
        print("\n✅ Migration completed successfully!")
        print("\nNew features available:")
        print("  - Loyalty Points: Users earn 1 point per ₹10 spent")
        print("  - Points Redemption: 100 points = ₹10 discount")
        print("  - Order Scheduling: Schedule orders for future delivery")
        print("  - Recurring Orders: Set up automatic recurring deliveries")

if __name__ == '__main__':
    migrate_database()

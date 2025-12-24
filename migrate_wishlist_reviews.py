"""
Proper migration script to add new columns to existing database
"""
from flask import Flask
from extensions import db
from sqlalchemy import text

# Create app instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    # Add new columns to product table
    try:
        with db.engine.connect() as conn:
            # Check if columns exist first
            result = conn.execute(text("PRAGMA table_info(product)"))
            existing_columns = [row[1] for row in result]
            
            print(f"Existing columns: {existing_columns}")
            
            # Add missing columns
            if 'description' not in existing_columns:
                conn.execute(text("ALTER TABLE product ADD COLUMN description VARCHAR(500)"))
                conn.commit()
                print("✓ Added 'description' column")
            
            if 'detailed_description' not in existing_columns:
                conn.execute(text("ALTER TABLE product ADD COLUMN detailed_description TEXT"))
                conn.commit()
                print("✓ Added 'detailed_description' column")
            
            if 'average_rating' not in existing_columns:
                conn.execute(text("ALTER TABLE product ADD COLUMN average_rating FLOAT DEFAULT 0.0"))
                conn.commit()
                print("✓ Added 'average_rating' column")
            
            if 'review_count' not in existing_columns:
                conn.execute(text("ALTER TABLE product ADD COLUMN review_count INTEGER DEFAULT 0"))
                conn.commit()
                print("✓ Added 'review_count' column")
        
        # Now create new tables
        db.create_all()
        print("✓ Created Wishlist and Review tables")
        
        print("\n✅ Database migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        raise

"""
Database migration script to add Address table and address_id to Order table
Run this script to update existing database
"""
from app import create_app
from extensions import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # Create Address table
        db.session.execute(text('''
            CREATE TABLE IF NOT EXISTS address (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                address_line1 VARCHAR(200) NOT NULL,
                address_line2 VARCHAR(200),
                city VARCHAR(100) NOT NULL,
                state VARCHAR(100) NOT NULL,
                pincode VARCHAR(20) NOT NULL,
                is_default BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user(id)
            )
        '''))
        
        # Check if address_id column exists in order table
        result = db.session.execute(text('PRAGMA table_info("order")'))
        columns = [row[1] for row in result]
        
        if 'address_id' not in columns:
            # Add address_id column to order table
            db.session.execute(text('ALTER TABLE "order" ADD COLUMN address_id INTEGER'))
            print("✓ Successfully added address_id column to Order table")
        else:
            print("✓ address_id column already exists in Order table")
        
        db.session.commit()
        print("✓ Successfully created Address table")
        print("✓ Database migration completed successfully!")
            
    except Exception as e:
        print(f"✗ Error during migration: {e}")
        db.session.rollback()

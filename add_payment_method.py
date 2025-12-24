"""
Database migration script to add payment_method column to Order table
Run this script to update existing database
"""
from app import create_app
from extensions import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # Check if column already exists
        result = db.session.execute(text('PRAGMA table_info("order")'))
        columns = [row[1] for row in result]
        
        if 'payment_method' not in columns:
            # Add the new column
            db.session.execute(text('ALTER TABLE "order" ADD COLUMN payment_method VARCHAR(50)'))
            db.session.commit()
            print("✓ Successfully added payment_method column to Order table")
        else:
            print("✓ payment_method column already exists")
            
    except Exception as e:
        print(f"✗ Error during migration: {e}")
        db.session.rollback()

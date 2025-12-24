"""
Fix database schema by adding missing columns for loyalty and scheduling features.
This script uses ALTER TABLE to add columns to existing tables.
"""
import sqlite3
import os

def fix_database():
    db_path = 'instance/grocery.db'
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Starting database schema fix...")
    
    # Add loyalty_points to user table
    try:
        cursor.execute("ALTER TABLE user ADD COLUMN loyalty_points INTEGER DEFAULT 0")
        print("✓ Added loyalty_points column to user table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("✓ loyalty_points column already exists in user table")
        else:
            print(f"✗ Error adding loyalty_points: {e}")
    
    # Add points_earned to order table
    try:
        cursor.execute("ALTER TABLE 'order' ADD COLUMN points_earned INTEGER DEFAULT 0")
        print("✓ Added points_earned column to order table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("✓ points_earned column already exists in order table")
        else:
            print(f"✗ Error adding points_earned: {e}")
    
    # Add points_redeemed to order table
    try:
        cursor.execute("ALTER TABLE 'order' ADD COLUMN points_redeemed INTEGER DEFAULT 0")
        print("✓ Added points_redeemed column to order table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("✓ points_redeemed column already exists in order table")
        else:
            print(f"✗ Error adding points_redeemed: {e}")
    
    # Add scheduled_delivery_date to order table
    try:
        cursor.execute("ALTER TABLE 'order' ADD COLUMN scheduled_delivery_date DATETIME")
        print("✓ Added scheduled_delivery_date column to order table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("✓ scheduled_delivery_date column already exists in order table")
        else:
            print(f"✗ Error adding scheduled_delivery_date: {e}")
    
    # Add delivery_time_slot to order table
    try:
        cursor.execute("ALTER TABLE 'order' ADD COLUMN delivery_time_slot VARCHAR(50)")
        print("✓ Added delivery_time_slot column to order table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("✓ delivery_time_slot column already exists in order table")
        else:
            print(f"✗ Error adding delivery_time_slot: {e}")
    
    # Create loyalty_transaction table if not exists
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS loyalty_transaction (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                order_id INTEGER,
                points INTEGER NOT NULL,
                transaction_type VARCHAR(20) NOT NULL,
                description VARCHAR(200),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user(id),
                FOREIGN KEY (order_id) REFERENCES 'order'(id)
            )
        """)
        print("✓ Created loyalty_transaction table")
    except sqlite3.OperationalError as e:
        print(f"✗ Error creating loyalty_transaction table: {e}")
    
    # Create scheduled_order table if not exists
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scheduled_order (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                scheduled_date DATETIME NOT NULL,
                delivery_time_slot VARCHAR(50) NOT NULL,
                is_recurring BOOLEAN DEFAULT 0,
                recurrence_frequency VARCHAR(20),
                next_delivery_date DATETIME,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                items_json TEXT NOT NULL,
                total_price FLOAT NOT NULL,
                address_id INTEGER,
                payment_method VARCHAR(50),
                FOREIGN KEY (user_id) REFERENCES user(id),
                FOREIGN KEY (address_id) REFERENCES address(id)
            )
        """)
        print("✓ Created scheduled_order table")
    except sqlite3.OperationalError as e:
        print(f"✗ Error creating scheduled_order table: {e}")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Database schema fix completed!")
    print("\nPlease restart your Flask application for changes to take effect.")

if __name__ == '__main__':
    fix_database()

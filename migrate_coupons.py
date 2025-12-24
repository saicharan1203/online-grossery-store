import sqlite3
from datetime import datetime

def migrate_coupons():
    conn = sqlite3.connect('instance/grocery.db')
    cursor = conn.cursor()
    
    try:
        # Create Coupon table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS coupon (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code VARCHAR(20) NOT NULL UNIQUE,
            discount_type VARCHAR(20) NOT NULL,
            discount_value FLOAT NOT NULL,
            valid_from DATETIME,
            valid_to DATETIME,
            active BOOLEAN DEFAULT 1,
            usage_limit INTEGER,
            used_count INTEGER DEFAULT 0
        )
        ''')
        print("Created coupon table")
    except sqlite3.OperationalError as e:
        print(f"Error creating table: {e}")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    migrate_coupons()

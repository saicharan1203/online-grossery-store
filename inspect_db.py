import sqlite3
import os

db_path = 'instance/grocery.db'
if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    # Try root
    db_path = 'grocery.db'
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path} either")
        exit(1)

print(f"Inspecting {db_path}")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

if tables:
    for table in tables:
        print(f"\nSchema for {table[0]}:")
        cursor.execute(f"PRAGMA table_info({table[0]})")
        columns = cursor.fetchall()
        for col in columns:
            print(col)

conn.close()

import sqlite3

def migrate():
    conn = sqlite3.connect('instance/grocery.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE user ADD COLUMN email VARCHAR(120)")
        print("Added email column")
    except sqlite3.OperationalError:
        print("Email column might already exist")

    try:
        cursor.execute("ALTER TABLE user ADD COLUMN reset_token VARCHAR(100)")
        print("Added reset_token column")
    except sqlite3.OperationalError:
        print("reset_token column might already exist")

    try:
        cursor.execute("ALTER TABLE user ADD COLUMN reset_token_expiration DATETIME")
        print("Added reset_token_expiration column")
    except sqlite3.OperationalError:
        print("reset_token_expiration column might already exist")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    migrate()

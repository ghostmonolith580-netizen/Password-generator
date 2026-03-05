import sqlite3
import secrets
import string
from datetime import datetime

class PasswordDatabase:
    def __init__(self, db_name="passwords.db"):
        """Initialize the database and create the table if it doesn't exist."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Create a table to store passwords."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vault (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def save_password(self, service, password):
        """Save a new password to the database."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO vault (service, password, created_at) VALUES (?, ?, ?)",
            (service, password, timestamp)
        )
        self.conn.commit()
        print(f"✅ Password for '{service}' saved to database.")

    def list_passwords(self):
        """Retrieve all stored passwords."""
        self.cursor.execute("SELECT service, password, created_at FROM vault")
        return self.cursor.fetchall()

    def __del__(self):
        """Close the connection when the object is destroyed."""
        self.conn.close()

def generate_password(length=16):
    """Generate a cryptographically secure password."""
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

def main():
    db = PasswordDatabase()
    
    print("--- 🔐 Secure Password Vault ---")
    service_name = input("Enter the service name (e.g. Github, Netflix): ")
    
    # Generate and save
    new_password = generate_password(20)
    db.save_password(service_name, new_password)
    
    print(f"Generated Password: {new_password}")
    print("\n--- 📂 Your Stored Passwords ---")
    
    rows = db.list_passwords()
    for row in rows:
        print(f"Service: {row[0]} | Pass: {row[1]} | Date: {row[2]}")

if __name__ == "__main__":
    main()
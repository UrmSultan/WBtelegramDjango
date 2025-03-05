import sqlite3
from cryptography.fernet import Fernet
import config


DB_NAME = config.DB_NAME

KEY=config.ENCRYPTION_KEY
cipher = Fernet(KEY)

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            wb_token TEXT
        )
    """)
    conn.commit()
    conn.close()

# Save user token (encrypted)
def save_user_token(user_id: int, token: str):
    encrypted_token = cipher.encrypt(token.encode())
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO users VALUES (?, ?)", (user_id, encrypted_token))
    conn.commit()
    conn.close()

# Get user token (decrypted)
def get_user_token(user_id:int) -> str:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT wb_token FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return cipher.decrypt(row[0]).decode() if row else None

# Initialize database on import
init_db()
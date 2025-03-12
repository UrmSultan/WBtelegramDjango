import sqlite3
from cryptography.fernet import Fernet
import config


DB_NAME = config.DB_NAME
KEY=config.ENCRYPTION_KEY
cipher = Fernet(KEY)

def init_db():
    """Инициализация БД"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Таблица токенов (Wildberries API)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            token_id INTEGER PRIMARY KEY AUTOINCREMENT,
            wb_token TEXT UNIQUE
        )
    """)

    # Таблица связи пользователей с токенами (заменили ошибку)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_tokens (
            user_id INTEGER,
            token_id INTEGER,
            FOREIGN KEY (token_id) REFERENCES tokens (token_id),
            UNIQUE(user_id, token_id)
        )
    """)

    conn.commit()
    conn.close()

# Save user token (encrypted)
def save_user_token(user_id: int, token: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT token_id FROM tokens WHERE wb_token = ?", (token,))
        token_row = cursor.fetchone()

        if token_row:
            token_id = token_row[0]
            print(f"🔹 Токен уже есть в базе: token_id={token_id}")
        else:
            cursor.execute("INSERT INTO tokens (wb_token) VALUES (?)", (token,))
            token_id = cursor.lastrowid
            print(f"✅ Новый токен сохранен: token_id={token_id}")

        cursor.execute(
            "INSERT OR IGNORE INTO user_tokens (user_id, token_id) VALUES (?, ?)",
            (user_id, token_id)
        )
        conn.commit()
        print(f"✅ Токен сохранён для user_id {user_id}")
    except Exception as e:
        print(f"⚠ Ошибка сохранения токена: {e}")
    finally:
        conn.close()

# Get user token (decrypted)
def get_user_token(user_id:int) -> str:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
            SELECT tokens.wb_token FROM tokens
            JOIN user_tokens ON tokens.token_id = user_tokens.token_id
            WHERE user_tokens.user_id = ?
            """, (user_id,)
    )
    row = cursor.fetchone()
    conn.close()

    token =  row[0] if row else None
    #print(f"🔍 Полученный токен для user_id {user_id}: {token}")
    return token


init_db()
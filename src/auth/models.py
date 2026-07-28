from passlib.context import CryptContext
from src.auth.database import get_connection

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_user(name, email, password):
    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute("""
        INSERT INTO users (name, email, password)
        VALUES (?, ?, ?)
    """, (name, email, hashed_password))

    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    return user
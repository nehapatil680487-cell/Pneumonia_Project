import sqlite3
import hashlib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_NAME = os.path.join(
    BASE_DIR,
    "users.db"
)

# =========================================================
# CONNECTION
# =========================================================

def get_connection():

    return sqlite3.connect(
        DB_NAME,
        check_same_thread=False
    )

# =========================================================
# PASSWORD HASH
# =========================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()

# =========================================================
# USER TABLE
# =========================================================

def create_user_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (

            username TEXT PRIMARY KEY,

            password TEXT NOT NULL

        )
        """
    )

    conn.commit()

    conn.close()

# =========================================================
# ADD USER
# =========================================================

def add_user(username, password):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users
            (username, password)

            VALUES (?, ?)
            """,
            (
                username,
                hash_password(password)
            )
        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()

# =========================================================
# CHECK USER
# =========================================================

def check_user(username, password):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT username
        FROM users

        WHERE username=?
        AND password=?
        """,
        (
            username,
            hash_password(password)
        )
    )

    user = cursor.fetchone()

    conn.close()

    return user

# =========================================================
# INITIALIZE
# =========================================================

create_user_table()
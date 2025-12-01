import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'users.db')


#fra chatgpt
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

#fra Claus eksempel fra undervisning
def init_db():
    """Initialize the database with the users table"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

#fra chatgpt - vi opretter medarbejdere
def seed_users():
    """Insert predefined users if table is empty"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) as count FROM users')
    count = cursor.fetchone()['count']

    if count == 0:
        cursor.executemany('''
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        ''', [
            ("alice", "password123", "reader"),
            ("bob", "password123", "editor"),
            ("carla", "password123", "admin")
        ])

        conn.commit()
        print("✔ Added default users to database.")
    else:
        print("✔ Users already exist. Seed skipped.")
    conn.close()


def get_all_users():
    """Get all users from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    conn.close()

    return [
        {
            'id': user['id'],
            'username': user['username'],
            'password': user['password'],
            'role': user['role']
        }
        for user in users
    ]

def find_user_by_username(username):
    """Find a user by their username"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    conn.close()

    if user:
        return {
            'id': user['id'],
            'username': user['username'],
            'password': user['password'],
            'role': user['role']
        }
    return None

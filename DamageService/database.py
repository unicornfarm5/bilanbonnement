import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'damage.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with the users table"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute
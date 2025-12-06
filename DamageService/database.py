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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS damage_levels (
                   id INT PRIMARY KEY,
                   level_name TEXT UNIQUE NOT NULL,
                   price INT NOT NULL
     )
 ''')
    
    levels = [
        ('ingen', 0),
        ('let', 500),
        ('middel', 1500),
        ('svær', 3000),
        ('kritisk', 5000)
    ]
    # Forklar hvad der sker her
    cursor.executemany('INSERT OR IGNORE INTO damage_levels (level_name, price) VALUES (?, ?)', levels) 

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS damage (
                   damage_report_id INT PRIMARY KEY AUTOINCREMENT,
                   damage_level_id INTEGER NOT NULL, -- Peger på niveauet af skaden
                   damage_description TEXT,
                   damage_price INT,
                   licensplate TEXT, --mangler foreign key, men hvad menes der?
                   order_id INT,
                   FOREIGN KEY (damage_level_id) REFERENCES damage_levels(id) --må kun indeholde ID'er der eksisterer i damage_levels tabel
                   created_at (DATETIME DEFAULT current_timestamp)
                   )
                ''')
    conn.commit()
    conn.close()
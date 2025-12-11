import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'damage.db')

"""Her oprettes connection"""
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("PRAGMA foreign_keys = ON") # Aktiverer FK-constraints
    cursor = conn.cursor()

    # Opret opslagstabeller, hvis de ikke findes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS damage_levels (
            level_id INTEGER PRIMARY KEY AUTOINCREMENT,
            level_name TEXT UNIQUE NOT NULL,
            price INT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS damage (
            damage_report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            damage_level_id INTEGER NOT NULL,
            damage_description TEXT,
            damage_price INT,
            licensplate TEXT NOT NULL,
            order_id INT,
            created_at DATETIME DEFAULT current_timestamp,
            FOREIGN KEY (damage_level_id) REFERENCES damage_levels(level_id)
        )
    ''')

    conn.commit()
    conn.close()

# Seed af tabeller så de ikke er tomme - fra chatten
def seed_damages():
    """Indsæt test-data i damage-tabel hvis den er tom"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Sørg for at damage_levels er udfyldt inden vi inserter skader
    levels = [
        ('ingen', 0),
        ('let', 500),
        ('middel', 1500),
        ('svær', 3000),
        ('kritisk', 5000)
    ]
    cursor.executemany('INSERT OR IGNORE INTO damage_levels (level_name, price) VALUES (?, ?)', levels)
    conn.commit()
    
    # Tjek om tabel allerede har data
    cursor.execute('SELECT COUNT(*) as count FROM damage')
    count = cursor.fetchone()['count']
    
    if count == 0:
        # Test-data — matcher RentalService ordre og nummerplader
        damages_data = [
            (2, 'Ridse på siden', 500, 'AB12345', 1),           # order_id 1, plade AB12345
            (3, 'Knust forlygte', 1500, 'CD67890', 2),          # order_id 2, plade CD67890
            (2, 'Dent i døren', 500, 'EF11223', 3),             # order_id 3, plade EF11223
            (4, 'Knuste ruder', 3000, 'GH44556', 4),            # order_id 4, plade GH44556
            (5, 'Motorskade', 5000, 'IJ77889', 5),              # order_id 5, plade IJ77889
            (1, 'Lidt rust', 0, 'KL99001', 6),                  # order_id 6, plade KL99001
            (3, 'Revnet rude', 1500, 'MN22334', 7),             # order_id 7, plade MN22334
        ]
        
        cursor.executemany('''
            INSERT INTO damage (damage_level_id, damage_description, damage_price, licensplate, order_id)
            VALUES (?, ?, ?, ?, ?)
        ''', damages_data)
        
        conn.commit()
        print("✔ Added test damages to database.")
    else:
        print("✔ Damages already exist. Seed skipped.")
    
    conn.close()

#Slå pris op fra damage_levels
def get_price_from_level(level_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT price FROM damage_levels WHERE level_id = ?', (level_id,))
    row = cursor.fetchone() #??
    return row['price'] if row else None

#Indsæt skade i damage-tabel
def insert_damage(damage_level_id, damage_description, damage_price, licensplate, order_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO damage (damage_level_id, damage_description, damage_price, licensplate, order_id, created_at)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
    ''', (damage_level_id, damage_description, damage_price, licensplate, order_id)) #???
    conn.commit()
    last_id = cursor.lastrowid #Gemmer sidste givne id
    conn.close()
    return last_id #Viser sidste givne id

#Hent alle skader for en bil med pris-info
def get_damage_history(license_plate):
    conn = get_db_connection()
    cursor = conn.cursor() #SELECT taget fra chatten
    cursor.execute(''' 
        SELECT d.damage_report_id, d.damage_description, d.damage_price, d.order_id, d.created_at,
             dl.level_name AS damage_level_name, dl.price AS level_price
         FROM damage d
         LEFT JOIN damage_levels dl ON d.damage_level_id = dl.level_id
        WHERE d.licensplate = ?
        ORDER BY d.created_at DESC
    ''', (license_plate,))
    rows = cursor. fetchall()
    conn.close()
    return [dict(r) for r in rows] #???
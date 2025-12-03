import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'rental.db')


#fra chatgpt
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

#fra Claus eksempel fra undervisning
def init_db():
    """Initialize the database with the rental table"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Drop table if it exists
    cursor.execute('DROP TABLE IF EXISTS rental;')

    # Create table
    cursor.execute('''
        CREATE TABLE rental (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT UNIQUE NOT NULL,
            license_plate TEXT NOT NULL,
            rental_start DATE NOT NULL,
            rental_end DATE NOT NULL,
            rental_type TEXT NOT NULL CHECK (rental_type IN ('leasing', 'abonnement')),
            price_per_month REAL NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


#chatGPT er brugt til at genere data
#
def seed_rentals():
    """Insert predefined rentals if table is empty"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) as count FROM rental')
    count = cursor.fetchone()['count']

    if count == 0:
        rentals_data = [
            ('CUST001', 'AB12345', '2023-01-15', '2023-04-15', 'leasing', 2899),
            ('CUST002', 'CD67890', '2023-02-01', '2023-08-01', 'abonnement', 3199),
            ('CUST003', 'EF11223', '2023-03-10', '2023-12-10', 'leasing', 3499),
            ('CUST004', 'GH44556', '2023-01-05', '2024-01-05', 'abonnement', 2799),
            ('CUST005', 'IJ77889', '2023-04-20', '2024-10-20', 'leasing', 2599),
            ('CUST006', 'KL99001', '2023-05-12', '2025-05-12', 'abonnement', 2999),
            ('CUST007', 'MN22334', '2023-06-18', '2026-12-18', 'leasing', 3399),
            ('CUST008', 'OP55667', '2023-07-22', '2024-01-22', 'abonnement', 3099),
            ('CUST009', 'QR88990', '2023-08-03', '2023-11-03', 'leasing', 2499),
            ('CUST010', 'ST11229', '2023-09-14', '2024-03-14', 'abonnement', 2699),
            ('CUST011', 'UV33445', '2023-10-01', '2025-04-01', 'leasing', 3599),
            ('CUST012', 'WX66778', '2023-10-28', '2026-04-28', 'abonnement', 2899),
            ('CUST013', 'YZ99012', '2023-11-11', '2026-05-11', 'leasing', 3299),
            ('CUST014', 'AA12399', '2023-12-02', '2024-02-02', 'abonnement', 2199),
            ('CUST015', 'BB45677', '2024-01-19', '2027-07-19', 'leasing', 3899),
        ]

        cursor.executemany('''
            INSERT INTO rental (
                customer_id, license_plate, rental_start, rental_end,
                rental_type, price_per_month
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', rentals_data)

        conn.commit()
        print("✔ Added rentals to database.")
    else:
        print("✔ rentals already exist. Seed skipped.")

    conn.close()



######## -- Endpoints -- #########
def get_all_rentals_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM rental")
    rentals = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rentals]
import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'customer.db')


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
    cursor.execute('DROP TABLE IF EXISTS customer;')

    cursor.execute('''
        CREATE TABLE customer (
            customer_id TEXT PRIMARY KEY,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            customer_phone INTEGER,
            order_id INTEGER,
            FOREIGN KEY(order_id) REFERENCES rental(order_id)
        )
                   ''')
    conn.commit()
    conn.close()

def seed_customers():
        """Insert predefined customers if table is empty"""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) as count FROM customer')
        count = cursor.fetchone()['count']

        if count == 0:
            customers_data = [
                ('CU001', 'Alice Jensen', 'alice.jensen@email.com', 12345678, 1),
                ('CU002', 'Brian Nielsen', 'brian.nielsen@email.com', 23456789, 2),
                ('CU003', 'Carla Hansen', 'carla.hansen@email.com', 34567890, 3),
                ('CU004', 'David Larsen', 'david.larsen@email.com', 45678901, 4),
                ('CU005', 'Emma Pedersen', 'emma.pedersen@email.com', 56789012, 5),
                ('CU006', 'Frederik Sørensen', 'frederik.sorensen@email.com', 67890123, 6),
                ('CU007', 'Gitte Madsen', 'gitte.madsen@email.com', 78901234, 7),
                ('CU008', 'Henrik Kristensen', 'henrik.kristensen@email.com', 89012345, 8),
                ('CU009', 'Isabella Thomsen', 'isabella.thomsen@email.com', 90123456, 9),
                ('CU010', 'Jakob Olsen', 'jakob.olsen@email.com', 11234567, 10),
                ('CU011', 'Katrine Poulsen', 'katrine.poulsen@email.com', 22345678, 11),
                ('CU012', 'Lars Andersen', 'lars.andersen@email.com', 33456789, 12),
                ('CU013', 'Maria Rasmussen', 'maria.rasmussen@email.com', 44567890, 13),
                ('CU014', 'Nikolaj Mortensen', 'nikolaj.mortensen@email.com', 55678901, 14),
                ('CU015', 'Olivia Kristoffersen', 'olivia.kristoffersen@email.com', 66789012, 15),
                ('CU016', 'Peter Holm', 'peter.holm@email.com', 77890123, None), #De sidste 3 kunder her har ikke en ordre tilknyttet ved app start
                ('CU017', 'Rikke Jensen', 'rikke.jensen@email.com', 88901234, None),
                ('CU018', 'Søren Møller', 'soeren.moeller@email.com', 99012345, None),
            ]

            cursor.executemany('''
                INSERT INTO customer (
                    customer_id, customer_name, customer_email, customer_phone, order_id
                ) VALUES (?, ?, ?, ?, ?)
            ''', customers_data)

            conn.commit()
            print("✔ Added customers to database.")
        else:
            print("✔ Customers already exist. Seed skipped.")

        conn.close()


######## -- Funktioner i databasen -- #########
def get_all_customers_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM customer")
        rentals = cursor.fetchall()
        rentals_list = [dict(row) for row in rentals]
        return rentals_list
    finally:
        conn.close()


def get_all_customer_id_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT order_id, customer_id FROM customer")
        rentals = cursor.fetchall()
        rentals_list = [dict(row) for row in rentals]
        return rentals_list
    finally:
        conn.close()
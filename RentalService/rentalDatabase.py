import sqlite3
import os
from flask import jsonify

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
            license_plate TEXT UNIQUE NOT NULL, -- Sat UNIQUE ind men skal måske laves om
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
    # ---- 40 rows from 2023 ----
    ('CU001', 'AB12345', '2023-01-05', '2024-01-05', 'leasing', 2899),
    ('CU002', 'CD67890', '2023-01-12', '2023-07-12', 'abonnement', 2599),
    ('CU003', 'EF11223', '2023-01-28', '2024-01-28', 'leasing', 3199),
    ('CU004', 'GH44556', '2023-02-03', '2023-11-03', 'abonnement', 2799),
    ('CU005', 'IJ77889', '2023-02-14', '2024-08-14', 'leasing', 3399),
    ('CU006', 'KL99001', '2023-02-27', '2024-02-27', 'abonnement', 2499),
    ('CU007', 'MN22334', '2023-03-05', '2025-03-05', 'leasing', 3599),
    ('CU008', 'OP55667', '2023-03-18', '2023-09-18', 'abonnement', 2299),
    ('CU009', 'QR88990', '2023-04-01', '2024-04-01', 'leasing', 3099),
    ('CU010', 'ST11229', '2023-04-12', '2023-12-12', 'abonnement', 2399),
    ('CU011', 'UV33445', '2023-04-29', '2024-10-29', 'leasing', 3499),
    ('CU012', 'WX66778', '2023-05-04', '2023-11-04', 'abonnement', 2199),
    ('CU013', 'YZ99012', '2023-05-17', '2025-05-17', 'leasing', 3799),
    ('CU014', 'AA12399', '2023-06-01', '2024-06-01', 'abonnement', 2599),
    ('CU015', 'BB45677', '2023-06-15', '2026-06-15', 'leasing', 3899),
    ('CU016', 'CC78901', '2023-06-30', '2023-12-30', 'abonnement', 2399),
    ('CU017', 'DD10101', '2023-07-09', '2024-07-09', 'leasing', 3199),
    ('CU018', 'EE20201', '2023-07-22', '2025-01-22', 'abonnement', 2899),
    ('CU019', 'FF30301', '2023-08-03', '2024-08-03', 'leasing', 2999),
    ('CU020', 'GG40401', '2023-08-17', '2023-11-17', 'abonnement', 2199),
    ('CU021', 'HH50501', '2023-09-05', '2024-09-05', 'leasing', 3499),
    ('CU022', 'II60601', '2023-09-19', '2026-03-19', 'abonnement', 2799),
    ('CU023', 'JJ70701', '2023-10-01', '2024-04-01', 'leasing', 2599),
    ('CU024', 'KK80801', '2023-10-14', '2023-12-14', 'abonnement', 2299),
    ('CU025', 'LL90901', '2023-10-29', '2025-10-29', 'leasing', 3599),
    ('CU026', 'MM01001', '2023-11-06', '2024-05-06', 'abonnement', 2399),
    ('CU027', 'NN11101', '2023-11-21', '2026-11-21', 'leasing', 3899),
    ('CU028', 'OO21201', '2023-12-01', '2024-06-01', 'abonnement', 2599),
    ('CU029', 'PP31301', '2023-12-12', '2024-12-12', 'leasing', 2999),
    ('CU030', 'QQ41401', '2023-12-20', '2025-06-20', 'abonnement', 2899),
    ('CU031', 'RR51501', '2023-03-21', '2024-03-21', 'leasing', 3199),
    ('CU032', 'SS61601', '2023-04-11', '2023-10-11', 'abonnement', 2399),
    ('CU033', 'TT71701', '2023-05-23', '2024-11-23', 'leasing', 3499),
    ('CU034', 'UU81801', '2023-06-07', '2023-09-07', 'abonnement', 2199),
    ('CU035', 'VV91901', '2023-07-19', '2026-01-19', 'leasing', 3799),
    ('CU036', 'WW02001', '2023-08-01', '2023-12-01', 'abonnement', 2499),
    ('CU037', 'XX12101', '2023-09-10', '2024-09-10', 'leasing', 3199),
    ('CU038', 'YY22201', '2023-10-25', '2024-04-25', 'abonnement', 2399),
    ('CU039', 'ZZ32301', '2023-11-14', '2025-11-14', 'leasing', 3599),
    ('CU040', 'AB42401', '2023-12-27', '2024-06-27', 'abonnement', 2599),
    # ---- 110 rows from 2024–2025 ----
    ('CU041', 'AB12101', '2024-01-05', '2025-01-05', 'leasing', 2999),
    ('CU042', 'CD23201', '2024-01-15', '2024-07-15', 'abonnement', 2499),
    ('CU043', 'EF34301', '2024-01-28', '2026-01-28', 'leasing', 3399),
    ('CU044', 'GH45401', '2024-02-03', '2024-11-03', 'abonnement', 2699),
    ('CU045', 'IJ56501', '2024-02-12', '2025-08-12', 'leasing', 3299),
    ('CU046', 'KL67601', '2024-02-27', '2024-09-27', 'abonnement', 2399),
    ('CU047', 'MN78701', '2024-03-05', '2026-03-05', 'leasing', 3499),
    ('CU048', 'OP89801', '2024-03-18', '2025-03-18', 'abonnement', 2599),
    ('CU049', 'QR90901', '2024-03-29', '2025-03-29', 'leasing', 3099),
    ('CU050', 'ST01002', '2024-04-04', '2024-10-04', 'abonnement', 2299),
    ('CU051', 'UV11102', '2024-04-18', '2026-04-18', 'leasing', 3599),
    ('CU052', 'WX21202', '2024-04-29', '2025-10-29', 'abonnement', 2699),
    ('CU053', 'YZ31302', '2024-05-07', '2024-11-07', 'leasing', 2499),
    ('CU054', 'AA41402', '2024-05-20', '2027-05-20', 'abonnement', 3199),
    ('CU055', 'BB51502', '2024-06-02', '2026-06-02', 'leasing', 3399),
    ('CU056', 'CC61602', '2024-06-17', '2025-12-17', 'abonnement', 2799),
    ('CU057', 'DD71702', '2024-06-29', '2026-06-29', 'leasing', 3599),
    ('CU058', 'EE81802', '2024-07-14', '2025-01-14', 'abonnement', 2399),
    ('CU059', 'FF91902', '2024-07-28', '2027-07-28', 'leasing', 3899),
    ('CU060', 'GG02003', '2024-08-09', '2024-12-09', 'abonnement', 2299),
    ('CU061', 'HH12103', '2024-08-22', '2026-02-22', 'leasing', 3299),
    ('CU062', 'II22203', '2024-09-05', '2025-09-05', 'abonnement', 2599),
    ('CU063', 'JJ32303', '2024-09-17', '2027-09-17', 'leasing', 3799),
    ('CU064', 'KK42403', '2024-09-29', '2025-03-29', 'abonnement', 2499),
    ('CU065', 'LL52503', '2024-10-11', '2026-10-11', 'leasing', 3499),
    ('CU066', 'MM62603', '2024-10-25', '2025-04-25', 'abonnement', 2399),
    ('CU067', 'NN72703', '2024-11-06', '2026-11-06', 'leasing', 3599),
    ('CU068', 'OO82803', '2024-11-20', '2025-05-20', 'abonnement', 2599),
    ('CU069', 'PP92903', '2024-12-03', '2026-12-03', 'leasing', 3199),
    ('CU070', 'QQ03004', '2024-12-18', '2025-06-18', 'abonnement', 2299),
    ('CU071', 'RR13104', '2025-01-03', '2026-01-03', 'leasing', 2999),
    ('CU072', 'SS23204', '2025-01-15', '2027-01-15', 'abonnement', 2899),
    ('CU073', 'TT33304', '2025-01-27', '2025-11-27', 'leasing', 2699),
    ('CU074', 'UU43404', '2025-02-10', '2026-02-10', 'abonnement', 2599),
    ('CU075', 'VV53504', '2025-02-22', '2028-02-22', 'leasing', 3799),
    ('CU076', 'WW63604', '2025-03-03', '2025-09-03', 'abonnement', 2299),
    ('CU077', 'XX73704', '2025-03-19', '2027-03-19', 'leasing', 3399),
    ('CU078', 'YY83804', '2025-03-30', '2026-03-30', 'abonnement', 2899),
    ('CU079', 'ZZ93904', '2025-04-12', '2026-04-12', 'leasing', 2999),
    ('CU080', 'AB04005', '2025-04-25', '2025-10-25', 'abonnement', 2499),
    ('CU081', 'CD14105', '2025-05-07', '2028-05-07', 'leasing', 3899),
    ('CU082', 'EF24205', '2025-05-21', '2026-05-21', 'abonnement', 2599),
    ('CU083', 'GH34305', '2025-06-04', '2025-12-04', 'leasing', 2399),
    ('CU084', 'IJ44405', '2025-06-18', '2027-06-18', 'abonnement', 3299),
    ('CU085', 'KL54505', '2025-07-01', '2026-07-01', 'leasing', 2899),
    ('CU086', 'MN64605', '2025-07-15', '2025-11-15', 'abonnement', 2199),
    ('CU087', 'OP74705', '2025-07-29', '2027-07-29', 'leasing', 3499),
    ('CU088', 'QR84805', '2025-08-12', '2026-08-12', 'abonnement', 2799),
    ('CU089', 'ST94905', '2025-08-26', '2028-08-26', 'leasing', 3999),
    ('CU090', 'UV05006', '2025-09-09', '2025-12-09', 'abonnement', 2399),
    ('CU091', 'WX15106', '2025-09-22', '2027-09-22', 'leasing', 3599),
    ('CU092', 'YZ25206', '2025-10-05', '2026-04-05', 'abonnement', 2499),
    ('CU093', 'AA35306', '2025-10-20', '2027-10-20', 'leasing', 3299),
    ('CU094', 'BB45406', '2025-10-31', '2026-10-31', 'abonnement', 2799),
    ('CU095', 'CC55506', '2025-11-13', '2028-11-13', 'leasing', 3899),
    ('CU096', 'DD65606', '2025-11-27', '2026-05-27', 'abonnement', 2599),
    ('CU097', 'EE75706', '2025-12-09', '2027-12-09', 'leasing', 3499),
    ('CU098', 'FF85806', '2025-12-21', '2026-12-21', 'abonnement', 2799),
    ('CU099', 'GG95906', '2024-01-03', '2026-01-03', 'leasing', 3199),
    ('CU100', 'HH06007', '2024-01-19', '2024-07-19', 'abonnement', 2399),
    # Rows 101–150
    ('CU101', 'IJ16107', '2024-02-01', '2026-02-01', 'leasing', 3499),
    ('CU102', 'KL26207', '2024-02-14', '2024-08-14', 'abonnement', 2599),
    ('CU103', 'MN36307', '2024-02-28', '2025-02-28', 'leasing', 2899),
    ('CU104', 'OP46407', '2024-03-12', '2026-03-12', 'abonnement', 2799),
    ('CU105', 'QR56507', '2024-03-26', '2024-12-26', 'leasing', 2699),
    ('CU106', 'ST66607', '2024-04-08', '2026-10-08', 'abonnement', 3199),
    ('CU107', 'UV76707', '2024-04-22', '2025-04-22', 'leasing', 2999),
    ('CU108', 'WX86807', '2024-05-06', '2024-11-06', 'abonnement', 2499),
    ('CU109', 'YZ96907', '2024-05-20', '2027-05-20', 'leasing', 3899),
    ('CU110', 'AA07008', '2024-06-01', '2025-12-01', 'abonnement', 2799),
    ('CU111', 'BB17108', '2024-06-15', '2026-06-15', 'leasing', 3599),
    ('CU112', 'CC27208', '2024-06-29', '2024-09-29', 'abonnement', 2199),
    ('CU113', 'DD37308', '2024-07-12', '2026-07-12', 'leasing', 3299),
    ('CU114', 'EE47408', '2024-07-26', '2025-07-26', 'abonnement', 2599),
    ('CU115', 'FF57508', '2024-08-09', '2027-08-09', 'leasing', 3799),
    ('CU116', 'GG67608', '2024-08-23', '2024-11-23', 'abonnement', 2399),
    ('CU117', 'HH77708', '2024-09-04', '2026-09-04', 'leasing', 3499),
    ('CU118', 'II87808', '2024-09-18', '2025-03-18', 'abonnement', 2499),
    ('CU119', 'JJ97908', '2024-10-01', '2026-10-01', 'leasing', 3199),
    ('CU120', 'KK08009', '2024-10-14', '2025-04-14', 'abonnement', 2399),
    ('CU121', 'LL18109', '2024-10-27', '2027-10-27', 'leasing', 3899),
    ('CU122', 'MM28209', '2024-11-08', '2025-11-08', 'abonnement', 2599),
    ('CU123', 'NN38309', '2024-11-21', '2026-11-21', 'leasing', 3499),
    ('CU124', 'OO48409', '2024-12-04', '2025-06-04', 'abonnement', 2399),
    ('CU125', 'PP58509', '2024-12-18', '2027-12-18', 'leasing', 3799),
    ('CU126', 'QQ68609', '2025-01-02', '2026-01-02', 'abonnement', 2699),
    ('CU127', 'RR78709', '2025-01-16', '2025-07-16', 'leasing', 2599),
    ('CU128', 'SS88809', '2025-01-30', '2027-01-30', 'abonnement', 3199),
    ('CU129', 'TT98909', '2025-02-12', '2026-02-12', 'leasing', 2899),
    ('CU130', 'UU09010', '2025-02-25', '2025-11-25', 'abonnement', 2399),
    ('CU131', 'VV19110', '2025-03-07', '2027-03-07', 'leasing', 3599),
    ('CU132', 'WW29210', '2025-03-19', '2026-03-19', 'abonnement', 2699),
    ('CU133', 'XX39310', '2025-04-01', '2028-04-01', 'leasing', 3999),
    ('CU134', 'YY49410', '2025-04-14', '2025-10-14', 'abonnement', 2299),
    ('CU135', 'ZZ59510', '2025-04-28', '2027-04-28', 'leasing', 3399),
    ('CU136', 'AB69610', '2025-05-12', '2026-05-12', 'abonnement', 2799),
    ('CU137', 'CD79710', '2025-05-26', '2028-05-26', 'leasing', 3799),
    ('CU138', 'EF89810', '2025-06-06', '2025-12-06', 'abonnement', 2499),
    ('CU139', 'GH99910', '2025-06-21', '2027-06-21', 'leasing', 3599),
    ('CU140', 'IJ00011', '2025-07-02', '2026-07-02', 'abonnement', 2699),
    ('CU141', 'KL10111', '2025-07-16', '2025-12-16', 'leasing', 2599),
    ('CU142', 'MN20211', '2025-07-28', '2027-07-28', 'abonnement', 2999),
    ('CU143', 'OP30311', '2025-08-09', '2026-02-09', 'leasing', 2799),
    ('CU144', 'QR40411', '2025-08-23', '2025-11-23', 'abonnement', 2199),
    ('CU145', 'ST50511', '2025-09-04', '2027-09-04', 'leasing', 3299),
    ('CU146', 'UV60611', '2025-09-17', '2026-03-17', 'abonnement', 2599),
    ('CU147', 'WX70711', '2025-09-30', '2027-09-30', 'leasing', 3499),
    ('CU148', 'YZ80811', '2025-10-13', '2026-10-13', 'abonnement', 2699),
    ('CU149', 'AA90911', '2025-10-27', '2028-10-27', 'leasing', 3899),
    ('CU150', 'BB01012', '2025-11-08', '2026-05-08', 'abonnement', 2399)
    ]
    cursor.executemany('''
            INSERT INTO rental (
                customer_id, license_plate, rental_start, rental_end,
                rental_type, price_per_month
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', rentals_data)

    conn.commit()
    print("✔ Added rentals to database.")
    conn.close()



######## -- Funktioner i databasen -- #########
def get_all_rentals_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM rental")
        rentals = cursor.fetchall()
        return [dict(row) for row in rentals]
    finally:
        conn.close() #sørger for at vi altid lukker connection så der ikke er en forespørgsel der holder låsen


#med hjælp fra chatGPT til at skrive query korrekt til SQLite
def get_one_rental_db(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Brug parameter substitution for at undgå SQL-injection
        cursor.execute("SELECT * FROM rental WHERE order_id = ?", (order_id,))
        rental = cursor.fetchone()  # kun én lejeaftale
        if rental:
            return dict(rental)
        return None
    finally:
        conn.close()

def add_rentals_db(
        customer_id, license_plate, rental_start, rental_end, rental_type, price_per_month
        ):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        sql = """
            INSERT INTO rental (
                customer_id, 
                license_plate, 
                rental_start, 
                rental_end, 
                rental_type, 
                price_per_month
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, 
            (customer_id, license_plate, rental_start, rental_end, rental_type, price_per_month))
        conn.commit()

        # Henter alle rækker efter indsættelsen
        cursor.execute("SELECT * FROM rental")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


#Kan opdatere udvalgte felter angivet i updates class (i app.py)
#ide fra chatGPT
def update_rentals_db(order_id: int, updates: dict): 
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values())

        sql = f"UPDATE rental SET {set_clause} WHERE order_id = ?"

        cursor.execute(sql, values + [order_id])
        conn.commit()

        cursor.execute("SELECT * FROM rental WHERE order_id = ?", (order_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally: 
         conn.close()




from database.db import get_connection

def create_table():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            disease TEXT,
            confidence REAL,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()
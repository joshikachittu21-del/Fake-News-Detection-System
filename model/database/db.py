import sqlite3

DATABASE = "database/database.db"


def create_database():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            news TEXT,
            prediction TEXT
        )
    """)

    conn.commit()

    conn.close()

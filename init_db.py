import sqlite3

connection = sqlite3.connect("database.db")

connection.execute("""
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        short_code TEXT UNIQUE NOT NULL,
        original_url TEXT NOT NULL
        )
""")

connection.commit()
connection.close()

print("Database initialized.")
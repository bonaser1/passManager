import sqlite3

connect = sqlite3.connect('passwordsDataBase.db')
cursor = connect.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        app_name TEXT NOT NULL,
        user_name TEXT NOT NULL,
        password TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
""")

cursor.close()
connect.commit()
connect.close()
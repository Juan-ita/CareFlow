import sqlite3

connection = sqlite3.connect("careflow.db")

cursor = connection.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS patients (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   name TEXT NOT NULL,
   age INTEGER NOT NULL,
   phone TEXT NOT NULL
)
    """
)

connection.commit()
connection.close()
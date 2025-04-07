# models/database.py

import sqlite3
import os

def connect_db(db_path="data/database.db"):
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    try:
        db = sqlite3.connect(db_path)
        db.execute("PRAGMA foreign_keys = ON;")  # Enable foreign key support
        return db
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def create_tables(db):
    try:
        cursor = db.cursor()
        # Create tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                key INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                date TEXT,
                time TEXT,
                done INTEGER,
                duration INTEGER
            )
        ''')
        # Create subtasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subtasks (
                key INTEGER PRIMARY KEY AUTOINCREMENT,
                task_key INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                done INTEGER,
                FOREIGN KEY(task_key) REFERENCES tasks(key)
            )
        ''')
        db.commit()
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")

def close_db(db):
    try:
        db.close()
    except sqlite3.Error as e:
        print(f"Error closing database: {e}")

def init_db():
    """
    Initialize the database by connecting and creating tables if they don't exist.
    """
    db = connect_db()
    if db:
        create_tables(db)
        close_db(db)
        
if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
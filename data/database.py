# database/database.py

import sqlite3
import os

def connect_db(db_path="data/database.db"):
    """
    Établit la connexion à la base SQLite, crée le dossier data/ si besoin.
    """
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    try:
        db = sqlite3.connect(db_path)
        db.execute("PRAGMA foreign_keys = ON;")
        return db
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def create_tables(db):
    """
    Crée (si elles n'existent pas) les tables tasks et subtasks.
    """
    try:
        cursor = db.cursor()
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
    """Ferme la connexion DB."""
    if db:
        try:
            db.close()
        except sqlite3.Error as e:
            print(f"Error closing database: {e}")

def init_db():
    """Initialise la DB en créant les tables au besoin."""
    db = connect_db()
    if db:
        create_tables(db)
        close_db(db)

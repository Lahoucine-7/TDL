# database/database.py

import sqlite3
import os

def connect_db(db_path="data/database.db"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    try:
        db = sqlite3.connect(db_path)
        db.execute("PRAGMA foreign_keys = ON;")
        return db
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def create_tables(db):
    try:
        cursor = db.cursor()
        # Table Users (optionnel)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT,
                password TEXT,
                theme TEXT DEFAULT 'dark'
            )
        ''')
        # Table Projects
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            )
        ''')
        # Table Tasks (ajout de project_id)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                date TEXT,
                time TEXT,
                done INTEGER,
                duration INTEGER,
                project_id INTEGER,
                FOREIGN KEY(project_id) REFERENCES projects(id)
            )
        ''')
        # Table Subtasks
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subtasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                done INTEGER,
                FOREIGN KEY(task_id) REFERENCES tasks(id)
            )
        ''')
        # Table Settings (optionnel)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                key TEXT,
                value TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        db.commit()
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")

def close_db(db):
    if db:
        try:
            db.close()
        except sqlite3.Error as e:
            print(f"Error closing database: {e}")

def init_db():
    db = connect_db()
    if db:
        create_tables(db)
        close_db(db)

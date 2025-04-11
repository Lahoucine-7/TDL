"""
database.py

Provides functions to manage the SQLite database connection and table creation.
It creates the required database directories, connects to the database,
enables foreign key support, and creates the necessary tables if they don't exist.
"""

import sqlite3
import os

def connect_db(db_path: str = "data/database.db"):
    """
    Connects to the SQLite database at the specified path.
    Ensures that the directory exists and enables foreign key support.

    Args:
        db_path (str): The file path for the SQLite database.

    Returns:
        sqlite3.Connection or None: The database connection object or None if an error occurs.
    """
    # Create the directory if it does not exist.
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    try:
        db = sqlite3.connect(db_path)
        # Enable foreign key support.
        db.execute("PRAGMA foreign_keys = ON;")
        return db
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def create_tables(db: sqlite3.Connection):
    """
    Creates the necessary tables for the application (users, projects, tasks,
    subtasks, and settings) if they do not already exist.

    Args:
        db (sqlite3.Connection): The active database connection.
    """
    try:
        cursor = db.cursor()
        # Create Users table.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT UNIQUE,
                password TEXT,
                theme TEXT DEFAULT 'dark',
                created_at TEXT,
                updated_at TEXT,
                last_login TEXT
            )
        ''')
        # Create Projects table.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                created_at TEXT,
                updated_at TEXT,
                color TEXT,
                icon TEXT,
                position INTEGER
            )
        ''')
        # Create Tasks table.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                created_at TEXT,
                updated_at TEXT,
                due_date TEXT,
                time TEXT,
                duration INTEGER,
                priority TEXT,
                status TEXT,
                done INTEGER,
                project_id INTEGER,
                FOREIGN KEY(project_id) REFERENCES projects(id)
            )
        ''')
        # Create Subtasks table.
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
        # Create Settings table.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                key TEXT NOT NULL,
                value TEXT,
                created_at TEXT,
                updated_at TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        db.commit()
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")

def close_db(db: sqlite3.Connection):
    """
    Closes the database connection.

    Args:
        db (sqlite3.Connection): The database connection to close.
    """
    if db:
        try:
            db.close()
        except sqlite3.Error as e:
            print(f"Error closing database: {e}")

def init_db():
    """
    Initializes the database by connecting, creating required tables, then closing the connection.
    """
    db = connect_db()
    if db:
        create_tables(db)
        close_db(db)

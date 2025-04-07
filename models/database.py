import sqlite3
import os

def connect_db(db_path="data/database.db"):
    # Crée le dossier s'il n'existe pas
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    # Établit la connexion à la base de données SQLite
    try:
        db = sqlite3.connect(db_path)
        db.execute("PRAGMA foreign_keys = ON;")  # Activation des clés étrangères
        return db
    except sqlite3.Error as e:
        print(f"Erreur lors de la connexion à la base de données: {e}")
        return None

def create_tables(db):
    try:
        cursor = db.cursor()
        # Création de la table pour les tâches
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                key INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                description TEXT,
                date TEXT,
                heure TEXT,
                done INTEGER,
                duree INTEGER
            )
        ''')
        # Création de la table pour les sous-tâches
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subtasks (
                key INTEGER PRIMARY KEY AUTOINCREMENT,
                task_key INTEGER,
                titre TEXT NOT NULL,
                description TEXT,
                done INTEGER,
                FOREIGN KEY(task_key) REFERENCES tasks(key)
            )
        ''')
        db.commit()
    except sqlite3.Error as e:
        print(f"Erreur lors de la création des tables: {e}")

def close_db(db):
    try:
        db.close()
    except sqlite3.Error as e:
        print(f"Erreur lors de la fermeture de la base de données: {e}")

if __name__ == "__main__":
    db = connect_db()
    if db:
        create_tables(db)
        print("Tables créées avec succès.")
        close_db(db)
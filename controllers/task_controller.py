# controllers/task_controller.py

from models.task import Task
from models.subtask import Subtask
from models.database import connect_db, close_db

def execute_query(query, params=(), fetch=False):
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall() if fetch else None
        db.commit()
        lastrowid = cursor.lastrowid
        close_db(db)
        return result, lastrowid
    except Exception as e:
        print(f"Erreur lors de l'exécution de la requête: {e}")
        close_db(db)
        return None, None

# --- Fonctions pour les tâches ---

def ajouter_tache(task):
    query = """
        INSERT INTO tasks (titre, description, date, heure, duree, done)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    _, lastrowid = execute_query(query, (task.titre, task.description, task.date, task.done, task.heure, task.duree))
    return lastrowid

def modifier_tache(task):
    query = """
        UPDATE tasks 
        SET titre = ?, description = ?, date = ?, heure = ?, duree = ?, done = ?
        WHERE key = ?
    """
    execute_query(query, (task.titre, task.description, task.date, task.heure, task.duree, task.done, task.key))

def supprimer_tache(task_key):
    # Supprimer d'abord les sous-tâches associées
    execute_query("DELETE FROM subtasks WHERE task_key = ?", (task_key,))
    execute_query("DELETE FROM tasks WHERE key = ?", (task_key,))

def lister_taches():
    query = "SELECT key, titre, description, date, heure, duree FROM tasks"
    rows, _ = execute_query(query, fetch=True)
    tasks = []
    for row in rows:
        key, titre, description, date, heure, duree = row
        task = Task(titre=titre, description=description, date=date, heure=heure, duree=duree, key=key)
        task.subtasks = lister_subtasks(key)
        tasks.append(task)
    return tasks

# --- Fonctions pour les sous-tâches ---

def ajouter_subtask(subtask):
    query = """
        INSERT INTO subtasks (task_key, titre, description)
        VALUES (?, ?, ?)
    """
    _, lastrowid = execute_query(query, (subtask.task_key, subtask.titre, subtask.description))
    return lastrowid

def modifier_subtask(subtask):
    query = """
        UPDATE subtasks
        SET titre = ?, description = ?
        WHERE key = ?
    """
    execute_query(query, (subtask.titre, subtask.description, subtask.key))

def supprimer_subtask(subtask_key):
    query = "DELETE FROM subtasks WHERE key = ?"
    execute_query(query, (subtask_key,))

def lister_subtasks(task_key):
    query = "SELECT key, task_key, titre, description FROM subtasks WHERE task_key = ?"
    rows, _ = execute_query(query, (task_key,), fetch=True)
    subtasks = []
    for row in rows:
        key, task_key, titre, description = row
        subtasks.append(Subtask(task_key=task_key, titre=titre, description=description, key=key))
    return subtasks

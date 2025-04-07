# controllers/task_controller.py

from models.task import Task
from models.subtask import Subtask
from models.database import connect_db, close_db

def execute_query(query, params=(), fetch=False):
    """
    Executes an SQL query with the provided parameters.
    :param query: SQL query string.
    :param params: Tuple of parameters.
    :param fetch: Boolean indicating if fetchall() should be called.
    :return: Tuple (results, lastrowid).
    """
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
        print(f"Error executing query: {e}")
        close_db(db)
        return None, None

# --- Task functions ---

def add_task(task):
    query = """
        INSERT INTO tasks (title, description, date, time, duration, done)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    # Store 'done' as integer (0 or 1)
    _, lastrowid = execute_query(query, (task.title, task.description, task.date, task.time, task.duration, int(task.done)))
    return lastrowid

def update_task(task):
    query = """
        UPDATE tasks 
        SET title = ?, description = ?, date = ?, time = ?, duration = ?, done = ?
        WHERE key = ?
    """
    execute_query(query, (task.title, task.description, task.date, task.time, task.duration, int(task.done), task.key))

def delete_task(task_key):
    # Delete associated subtasks first
    execute_query("DELETE FROM subtasks WHERE task_key = ?", (task_key,))
    execute_query("DELETE FROM tasks WHERE key = ?", (task_key,))

def list_tasks():
    query = "SELECT key, title, description, date, time, duration, done FROM tasks"
    rows, _ = execute_query(query, fetch=True)
    tasks = []
    if rows:
        for row in rows:
            key, title, description, date, time_field, duration, done = row
            task = Task(title=title, description=description, date=date, time=time_field, duration=duration, key=key, done=bool(done))
            task.subtasks = list_subtasks(key)
            tasks.append(task)
    return tasks

# --- Subtask functions ---

def add_subtask(subtask):
    query = """
        INSERT INTO subtasks (task_key, title, description, done)
        VALUES (?, ?, ?, ?)
    """
    _, lastrowid = execute_query(query, (subtask.task_key, subtask.title, subtask.description, int(subtask.done)))
    return lastrowid

def update_subtask(subtask):
    query = """
        UPDATE subtasks
        SET title = ?, description = ?, done = ?
        WHERE key = ?
    """
    execute_query(query, (subtask.title, subtask.description, int(subtask.done), subtask.key))

def delete_subtask(subtask_key):
    query = "DELETE FROM subtasks WHERE key = ?"
    execute_query(query, (subtask_key,))

def list_subtasks(task_key):
    query = "SELECT key, task_key, title, description, done FROM subtasks WHERE task_key = ?"
    rows, _ = execute_query(query, (task_key,), fetch=True)
    subtasks = []
    if rows:
        for row in rows:
            key, task_key, title, description, done = row
            subtasks.append(Subtask(task_key=task_key, title=title, description=description, key=key, done=bool(done)))
    return subtasks

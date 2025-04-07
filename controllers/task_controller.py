# controllers/task_controller.py

from models.task import Task
from models.subtask import Subtask
from data.database import connect_db, close_db

class TaskController:
    """
    Contrôleur gérant la logique métier pour les tâches et sous-tâches.
    La vue (main_view) appelle ses méthodes pour créer/supprimer/éditer des tâches.
    """

    def execute_query(self, query, params=(), fetch=False):
        db = None
        try:
            db = connect_db()
            if not db:
                return (None, None)
            cursor = db.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall() if fetch else None
            db.commit()
            return (rows, cursor.lastrowid)
        except Exception as e:
            print(f"[TaskController] Error executing query: {e}")
            return (None, None)
        finally:
            close_db(db)

    def create_task(self, title: str, description: str = "", date=None, time=None, duration=None) -> bool:
        """
        Crée une nouvelle tâche. Retourne True si OK, False sinon.
        """
        if not title.strip():
            return False
        # Insertion en DB
        query = """
            INSERT INTO tasks (title, description, date, time, duration, done)
            VALUES (?, ?, ?, ?, ?, 0)
        """
        _, last_id = self.execute_query(query, (title, description, date, time, duration))
        return (last_id is not None)

    def list_tasks(self):
        """
        Retourne la liste de toutes les tâches, chargées depuis la DB,
        sous forme d'objets Task (chacune ayant ses subtasks).
        """
        query = "SELECT key, title, description, date, time, duration, done FROM tasks"
        rows, _ = self.execute_query(query, fetch=True)
        tasks = []
        if rows:
            for row in rows:
                key, title, desc, date, time_field, dur, done_val = row
                t = Task(
                    key=key,
                    title=title,
                    description=desc or "",
                    date=date,
                    time=time_field,
                    duration=dur,
                    done=bool(done_val)
                )
                # Charger subtasks
                t.subtasks = self.list_subtasks(t.key)
                tasks.append(t)
        return tasks

    def mark_task_done(self, task_key: int, is_done: bool = True):
        """
        Marque la tâche task_key comme (non) terminée.
        """
        query = "UPDATE tasks SET done = ? WHERE key = ?"
        self.execute_query(query, (1 if is_done else 0, task_key))

    def delete_task(self, task_key: int):
        """
        Supprime la tâche (et ses subtasks) identifiée par task_key.
        """
        self.execute_query("DELETE FROM subtasks WHERE task_key = ?", (task_key,))
        self.execute_query("DELETE FROM tasks WHERE key = ?", (task_key,))

    def update_task(self, task: Task):
        """
        Met à jour la tâche existante.
        """
        query = """
            UPDATE tasks
               SET title = ?, description = ?, date = ?, time = ?, duration = ?, done = ?
             WHERE key = ?
        """
        self.execute_query(query, (
            task.title,
            task.description,
            task.date,
            task.time,
            task.duration,
            int(task.done),
            task.key
        ))

    # Sous-tâches

    def list_subtasks(self, task_key: int):
        query = "SELECT key, title, description, done FROM subtasks WHERE task_key = ?"
        rows, _ = self.execute_query(query, (task_key,), fetch=True)
        subs = []
        if rows:
            for row in rows:
                skey, stitle, sdesc, sdone = row
                subs.append(Subtask(
                    key=skey,
                    task_key=task_key,
                    title=stitle,
                    description=sdesc,
                    done=bool(sdone)
                ))
        return subs

    def create_subtask(self, task_key: int, title: str, description: str = "") -> bool:
        if not title.strip():
            return False
        query = """
            INSERT INTO subtasks (task_key, title, description, done)
            VALUES (?, ?, ?, 0)
        """
        _, last_id = self.execute_query(query, (task_key, title, description))
        return (last_id is not None)

    def update_subtask(self, subtask: Subtask):
        query = """
            UPDATE subtasks
               SET title = ?, description = ?, done = ?
             WHERE key = ?
        """
        self.execute_query(query, (subtask.title, subtask.description, int(subtask.done), subtask.key))

    def delete_subtask(self, subtask_key: int):
        self.execute_query("DELETE FROM subtasks WHERE key = ?", (subtask_key,))

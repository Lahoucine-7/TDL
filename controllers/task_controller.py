# controllers/task_controller.py

from models.task import Task
from models.subtask import Subtask
from models.project import Project
from database.database import connect_db, close_db

class TaskController:
    """
    Contrôleur pour gérer les tâches, sous-tâches et projets.
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
            # Utilisation de logging serait préférable
            print(f"[TaskController] Error executing query: {e}")
            return (None, None)
        finally:
            close_db(db)

    # --- Tâches ---
    def create_task(self, title: str, description: str = "", date=None, time=None, duration=None, project_id=None) -> bool:
        if not title.strip():
            return False
        query = """
            INSERT INTO tasks (title, description, date, time, duration, done, project_id)
            VALUES (?, ?, ?, ?, ?, 0, ?)
        """
        _, last_id = self.execute_query(query, (title, description, date, time, duration, project_id))
        return last_id is not None

    def list_tasks(self, project_id=None):
        if project_id is None:
            query = "SELECT id, title, description, date, time, duration, done, project_id FROM tasks"
            rows, _ = self.execute_query(query, fetch=True)
        else:
            query = "SELECT id, title, description, date, time, duration, done, project_id FROM tasks WHERE project_id = ?"
            rows, _ = self.execute_query(query, (project_id,), fetch=True)
        tasks = []
        if rows:
            for row in rows:
                id_, title, desc, date, time_field, dur, done_val, proj_id = row
                t = Task(
                    id=id_,
                    title=title,
                    description=desc or "",
                    date=date,
                    time=time_field,
                    duration=dur,
                    done=bool(done_val),
                    project_id=proj_id
                )
                t.subtasks = self.list_subtasks(t.id)
                tasks.append(t)
        return tasks

    def mark_task_done(self, task_id: int, is_done: bool = True):
        query = "UPDATE tasks SET done = ? WHERE id = ?"
        self.execute_query(query, (1 if is_done else 0, task_id))

    def delete_task(self, task_id: int):
        self.execute_query("DELETE FROM subtasks WHERE task_id = ?", (task_id,))
        self.execute_query("DELETE FROM tasks WHERE id = ?", (task_id,))

    def update_task(self, task: Task):
        query = """
            UPDATE tasks
               SET title = ?, description = ?, date = ?, time = ?, duration = ?, done = ?, project_id = ?
             WHERE id = ?
        """
        self.execute_query(query, (
            task.title,
            task.description,
            task.date,
            task.time,
            task.duration,
            int(task.done),
            task.project_id,
            task.id
        ))

    # --- Sous-tâches ---
    def list_subtasks(self, task_id: int):
        query = "SELECT id, title, description, done FROM subtasks WHERE task_id = ?"
        rows, _ = self.execute_query(query, (task_id,), fetch=True)
        subs = []
        if rows:
            for row in rows:
                id_, title, desc, done_val = row
                subs.append(Subtask(
                    id=id_,
                    task_id=task_id,
                    title=title,
                    description=desc,
                    done=bool(done_val)
                ))
        return subs

    def create_subtask(self, task_id: int, title: str, description: str = "") -> bool:
        if not title.strip():
            return False
        query = """
            INSERT INTO subtasks (task_id, title, description, done)
            VALUES (?, ?, ?, 0)
        """
        _, last_id = self.execute_query(query, (task_id, title, description))
        return last_id is not None

    def update_subtask(self, subtask: Subtask):
        query = """
            UPDATE subtasks
               SET title = ?, description = ?, done = ?
             WHERE id = ?
        """
        self.execute_query(query, (subtask.title, subtask.description, int(subtask.done), subtask.id))

    def delete_subtask(self, subtask_id: int):
        query = "DELETE FROM subtasks WHERE id = ?"
        self.execute_query(query, (subtask_id,))

    # --- Projets ---
    def create_folder(self, name: str, description: str = "") -> bool:
        if not name.strip():
            return False
        query = "INSERT INTO projects (name, description) VALUES (?, ?)"
        _, last_id = self.execute_query(query, (name, description))
        return last_id is not None

    def list_folders(self):
        query = "SELECT id, name, description FROM projects"
        rows, _ = self.execute_query(query, fetch=True)
        folders = []
        if rows:
            from models.project import Project
            for row in rows:
                id_, name, description = row
                folders.append(Project(id=id_, name=name, description=description))
        return folders

    def update_folder(self, folder: Project):
        query = "UPDATE projects SET name = ?, description = ? WHERE id = ?"
        self.execute_query(query, (folder.name, folder.description, folder.id))

    def delete_folder(self, folder_id: int):
        # Optionnel : Vous pourriez vérifier ou transférer les tâches associées
        query = "DELETE FROM projects WHERE id = ?"
        self.execute_query(query, (folder_id,))

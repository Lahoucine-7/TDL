"""
task_controller.py

TaskController manages operations related to tasks and subtasks, including creation,
retrieval, update, and deletion of tasks along with their associated subtasks.
It also provides helper methods for marking tasks as done.
"""

from datetime import datetime
from models.task import Task
from models.subtask import Subtask
from models.project import Project
from database.database import connect_db, close_db

def get_current_timestamp() -> str:
    """
    Returns the current timestamp in ISO format.

    Returns:
        str: The current timestamp.
    """
    return datetime.now().isoformat()

class TaskController:
    """
    Controller for handling task operations, including CRUD actions for tasks and subtasks.
    """

    def execute_query(self, query: str, params: tuple = (), fetch: bool = False):
        """
        Executes a given SQL query.

        Args:
            query (str): The SQL query string.
            params (tuple): Parameters to substitute into the query.
            fetch (bool): If True, returns fetched rows.

        Returns:
            tuple: (rows, last_id) where rows is the query result (if fetched)
                   and last_id is the last inserted row ID.
        """
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
            # In production, replace print with proper logging.
            print(f"[TaskController] Error executing query: {e}")
            return (None, None)
        finally:
            close_db(db)

    # --- TASK METHODS ---

    def create_task(self, title: str, description: str = "", due_date = None, time = None,
                    duration = None, priority: str = "medium", status: str = "not started", project_id = None) -> bool:
        """
        Creates a new task in the database. Automatically sets the creation and update timestamps,
        and defaults status and priority if not provided.

        Args:
            title (str): The title of the task.
            description (str): The detailed description.
            due_date (str): The due date (ISO format).
            time (str): Specific time if applicable.
            duration (int): Estimated task duration in minutes.
            priority (str): Priority level (default "medium").
            status (str): Task status (default "not started").
            project_id (int): The ID of the associated project.
        
        Returns:
            bool: True if the task is created successfully, False otherwise.
        """
        if not title.strip():
            return False
        timestamp = get_current_timestamp()
        query = """
            INSERT INTO tasks (
                title, description, created_at, updated_at, due_date, time, duration, priority, status, done, project_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?)
        """
        params = (title, description, timestamp, timestamp, due_date, time, duration, priority, status, project_id)
        _, last_id = self.execute_query(query, params)
        return last_id is not None

    def list_tasks(self, project_id = None):
        """
        Retrieves tasks from the database, optionally filtered by a project ID.
        Also retrieves associated subtasks for each task.

        Args:
            project_id (int): Optional project ID to filter tasks.
        
        Returns:
            list: A list of Task objects.
        """
        if project_id is None:
            query = """
                SELECT id, title, description, created_at, updated_at, due_date, time, duration, priority, status, done, project_id 
                FROM tasks
            """
            rows, _ = self.execute_query(query, fetch=True)
        else:
            query = """
                SELECT id, title, description, created_at, updated_at, due_date, time, duration, priority, status, done, project_id 
                FROM tasks WHERE project_id = ?
            """
            rows, _ = self.execute_query(query, (project_id,), fetch=True)

        tasks = []
        if rows:
            for row in rows:
                (id_, title, desc, created_at, updated_at, due_date, time_field, dur,
                 priority, status, done_val, proj_id) = row
                t = Task(
                    id=id_,
                    title=title,
                    description=desc or "",
                    created_at=created_at,
                    updated_at=updated_at,
                    due_date=due_date,
                    time=time_field,
                    duration=dur,
                    priority=priority,
                    status=status,
                    done=bool(done_val),
                    project_id=proj_id
                )
                # Retrieve and assign associated subtasks.
                t.subtasks = self.list_subtasks(t.id)
                tasks.append(t)
        return tasks

    def mark_task_done(self, task_id: int, is_done: bool = True):
        """
        Marks a task as done (or not done) and updates its status accordingly.

        Args:
            task_id (int): The task's ID.
            is_done (bool): True if marking as done, False otherwise.
        """
        status = "completed" if is_done else "not started"
        query = "UPDATE tasks SET done = ?, status = ?, updated_at = ? WHERE id = ?"
        timestamp = get_current_timestamp()
        self.execute_query(query, (1 if is_done else 0, status, timestamp, task_id))

    def delete_task(self, task_id: int):
        """
        Deletes a task and all its associated subtasks from the database.

        Args:
            task_id (int): The ID of the task to delete.
        """
        self.execute_query("DELETE FROM subtasks WHERE task_id = ?", (task_id,))
        self.execute_query("DELETE FROM tasks WHERE id = ?", (task_id,))

    def update_task(self, task: Task):
        """
        Updates an existing task with new data. Updates the updated_at timestamp.

        Args:
            task (Task): The Task object containing updated information.
        """
        timestamp = get_current_timestamp()
        query = """
            UPDATE tasks
               SET title = ?, description = ?, updated_at = ?, due_date = ?, time = ?, duration = ?, priority = ?, status = ?, done = ?, project_id = ?
             WHERE id = ?
        """
        self.execute_query(query, (
            task.title,
            task.description,
            timestamp,
            task.due_date,
            task.time,
            task.duration,
            task.priority,
            task.status,
            int(task.done),
            task.project_id,
            task.id
        ))

    # --- SUBTASK METHODS ---

    def list_subtasks(self, task_id: int):
        """
        Retrieves all subtasks for a given task.

        Args:
            task_id (int): The parent task's ID.
        
        Returns:
            list: A list of Subtask objects.
        """
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
        """
        Creates a new subtask associated with a given task.

        Args:
            task_id (int): The parent task's ID.
            title (str): Title of the subtask.
            description (str): Optional description.
        
        Returns:
            bool: True if creation succeeded, False otherwise.
        """
        if not title.strip():
            return False
        query = """
            INSERT INTO subtasks (task_id, title, description, done)
            VALUES (?, ?, ?, 0)
        """
        _, last_id = self.execute_query(query, (task_id, title, description))
        return last_id is not None

    def update_subtask(self, subtask: Subtask):
        """
        Updates an existing subtask with new data.

        Args:
            subtask (Subtask): The Subtask object with updated information.
        """
        query = """
            UPDATE subtasks
               SET title = ?, description = ?, done = ?
             WHERE id = ?
        """
        self.execute_query(query, (subtask.title, subtask.description, int(subtask.done), subtask.id))

    def delete_subtask(self, subtask_id: int):
        """
        Deletes a subtask from the database.

        Args:
            subtask_id (int): The ID of the subtask to delete.
        """
        query = "DELETE FROM subtasks WHERE id = ?"
        self.execute_query(query, (subtask_id,))

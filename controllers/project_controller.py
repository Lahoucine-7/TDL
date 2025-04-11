"""
project_controller.py

The ProjectController class handles operations related to projects including
creation, listing, updating, and deletion. It uses a helper function to get the
current timestamp, and executes SQL queries with proper error handling.
"""

from datetime import datetime
import sqlite3
from models.project import Project
from database.database import connect_db, close_db

def get_current_timestamp() -> str:
    """
    Returns the current timestamp in ISO format.

    Returns:
        str: The current timestamp.
    """
    return datetime.now().isoformat()

class ProjectController:
    """
    ProjectController handles CRUD operations for Project objects.
    It creates, lists, updates, and deletes projects while ensuring that
    associated tasks/subtasks are handled appropriately.
    """

    def execute_query(self, query: str, params: tuple = (), fetch: bool = False):
        """
        Executes an SQL query with the provided parameters.

        Args:
            query (str): The SQL query string.
            params (tuple): Parameters to substitute into the query.
            fetch (bool): If True, fetches the result rows.

        Returns:
            tuple: (rows, last_id) where rows is the fetched data if any,
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
            print(f"[ProjectController] Error executing query: {e}")
            return (None, None)
        finally:
            close_db(db)

    def create_project(self, name: str, description: str = "", color: str = None,
                       icon: str = None, position: int = None) -> bool:
        """
        Creates a new project with the provided details.
        Automatically sets created_at and updated_at timestamps.

        Args:
            name (str): Name of the project.
            description (str): Project description.
            color (str): Optional color code.
            icon (str): Optional icon path.
            position (int): Optional display order position.

        Returns:
            bool: True if creation succeeded, False otherwise.
        """
        if not name.strip():
            return False
        timestamp = get_current_timestamp()
        query = """
            INSERT INTO projects (name, description, created_at, updated_at, color, icon, position)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        _, last_id = self.execute_query(query, (name, description, timestamp, timestamp, color, icon, position))
        return last_id is not None

    def list_projects(self):
        """
        Retrieves a list of projects from the database.

        Returns:
            list: List of Project objects.
        """
        query = "SELECT id, name, description, created_at, updated_at, color, icon, position FROM projects"
        rows, _ = self.execute_query(query, fetch=True)
        projects = []
        if rows:
            for row in rows:
                id_, name, description, created_at, updated_at, color, icon, position = row
                projects.append(Project(
                    id=id_,
                    name=name,
                    description=description,
                    created_at=created_at,
                    updated_at=updated_at,
                    color=color,
                    icon=icon,
                    position=position
                ))
        return projects

    def update_project(self, project: Project):
        """
        Updates a project in the database. Automatically updates the updated_at timestamp.

        Args:
            project (Project): The project object containing updated values.
        """
        timestamp = get_current_timestamp()
        query = """
            UPDATE projects
               SET name = ?, description = ?, updated_at = ?, color = ?, icon = ?, position = ?
             WHERE id = ?
        """
        self.execute_query(query, (
            project.name,
            project.description,
            timestamp,
            project.color,
            project.icon,
            project.position,
            project.id
        ))

    def delete_project(self, project_id: int, delete_tasks: bool = True):
        """
        Deletes a project. If delete_tasks is True, also deletes associated tasks and subtasks;
        otherwise, dissociates tasks by setting their project_id to NULL.

        Args:
            project_id (int): The project ID to delete.
            delete_tasks (bool): Flag to indicate whether to remove associated tasks/subtasks.
        """
        if delete_tasks:
            # Delete subtasks for tasks in the project.
            query_subtasks = "DELETE FROM subtasks WHERE task_id IN (SELECT id FROM tasks WHERE project_id = ?)"
            self.execute_query(query_subtasks, (project_id,))
            # Delete tasks for the project.
            query_tasks = "DELETE FROM tasks WHERE project_id = ?"
            self.execute_query(query_tasks, (project_id,))
        else:
            # Dissociate tasks from the project.
            query_update = "UPDATE tasks SET project_id = NULL WHERE project_id = ?"
            self.execute_query(query_update, (project_id,))
        # Finally, delete the project itself.
        query_project = "DELETE FROM projects WHERE id = ?"
        self.execute_query(query_project, (project_id,))

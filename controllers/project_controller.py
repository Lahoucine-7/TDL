# controllers/project_controller.py

from models.project import Project
from database.database import connect_db, close_db

class ProjectController:
    """
    Contrôleur pour gérer les projets.
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
            print(f"[ProjectController] Error executing query: {e}")
            return (None, None)
        finally:
            close_db(db)

    def create_project(self, name: str, description: str = "") -> bool:
        if not name.strip():
            return False
        query = "INSERT INTO projects (name, description) VALUES (?, ?)"
        _, last_id = self.execute_query(query, (name, description))
        return last_id is not None

    def list_projects(self):
        query = "SELECT id, name, description FROM projects"
        rows, _ = self.execute_query(query, fetch=True)
        projects = []
        if rows:
            for row in rows:
                id_, name, description = row
                projects.append(Project(id=id_, name=name, description=description))
        return projects

    def update_project(self, project: Project):
        query = "UPDATE projects SET name = ?, description = ? WHERE id = ?"
        self.execute_query(query, (project.name, project.description, project.id))

    def delete_project(self, project_id: int, delete_tasks: bool = True):
        if delete_tasks:
            # Supprimer les sous-tâches associées aux tâches du projet
            query_subtasks = "DELETE FROM subtasks WHERE task_id IN (SELECT id FROM tasks WHERE project_id = ?)"
            self.execute_query(query_subtasks, (project_id,))
            # Supprimer les tâches associées
            query_tasks = "DELETE FROM tasks WHERE project_id = ?"
            self.execute_query(query_tasks, (project_id,))
        else:
            # Dissocier les tâches du projet : définir project_id à NULL
            query_update = "UPDATE tasks SET project_id = NULL WHERE project_id = ?"
            self.execute_query(query_update, (project_id,))
        # Supprimer le projet
        query_project = "DELETE FROM projects WHERE id = ?"
        self.execute_query(query_project, (project_id,))
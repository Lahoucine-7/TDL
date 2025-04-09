# views/dashboard_view.py

import customtkinter as ctk
from controllers.task_controller import TaskController

class DashboardView(ctk.CTkFrame):
    """
    Dashboard affichant le nombre total de tâches, les tâches terminées, en retard et le nombre de projets.
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.controller = TaskController()
        self._create_widgets()
        self.refresh_dashboard()

    def _create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="Dashboard", font=("Roboto", 20))
        self.title_label.pack(pady=10)
        self.total_tasks_label = ctk.CTkLabel(self, text="Total Tasks: ", font=("Roboto", 16))
        self.total_tasks_label.pack(pady=5)
        self.done_tasks_label = ctk.CTkLabel(self, text="Completed Tasks: ", font=("Roboto", 16))
        self.done_tasks_label.pack(pady=5)
        self.overdue_tasks_label = ctk.CTkLabel(self, text="Overdue Tasks: ", font=("Roboto", 16))
        self.overdue_tasks_label.pack(pady=5)
        self.total_projects_label = ctk.CTkLabel(self, text="Total Projects: ", font=("Roboto", 16))
        self.total_projects_label.pack(pady=5)

    def refresh_dashboard(self):
        tasks = self.controller.list_tasks()
        total = len(tasks)
        done = len([t for t in tasks if t.done])
        # Pour "overdue", il faudrait comparer les dates – ici un placeholder
        overdue = 0  
        # Pour les projets, on pourrait appeler ProjectController; ici on simule
        from controllers.project_controller import ProjectController
        project_controller = ProjectController()
        projects = project_controller.list_projects()
        total_projects = len(projects)

        self.total_tasks_label.configure(text=f"Total Tasks: {total}")
        self.done_tasks_label.configure(text=f"Completed Tasks: {done}")
        self.overdue_tasks_label.configure(text=f"Overdue Tasks: {overdue}")
        self.total_projects_label.configure(text=f"Total Projects: {total_projects}")

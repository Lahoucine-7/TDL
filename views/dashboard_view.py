"""
dashboard_view.py

DashboardView shows a summary of tasks and projects:
  - Total tasks
  - Completed tasks
  - Overdue tasks
  - Total projects
It inherits from BaseView for consistent styling and translation.
"""

import customtkinter as ctk
from controllers.task_controller import TaskController
from controllers.project_controller import ProjectController
from views.base_view import BaseView
import theme

class DashboardView(BaseView):
    def __init__(self, master, *args, **kwargs):
        """
        Initializes DashboardView.

        Args:
            master: Parent widget.
            *args, **kwargs: Additional arguments.
        """
        super().__init__(master, *args, **kwargs)
        self.controller = TaskController()
        self.project_controller = ProjectController()
        self._create_widgets()
        self.refresh()

    def _create_widgets(self):
        """
        Creates and places dashboard labels.
        """
        self.title_label = ctk.CTkLabel(
            self,
            text=self.translations.t("dashboard"),
            font=("Roboto", 20)
        )
        self.title_label.pack(pady=10)
        
        self.total_tasks_label = ctk.CTkLabel(
            self,
            text=f"{self.translations.t('total_tasks') if hasattr(self.translations, 't') else 'Total Tasks:'}",
            font=("Roboto", 16)
        )
        self.total_tasks_label.pack(pady=5)
        
        self.done_tasks_label = ctk.CTkLabel(
            self,
            text=f"{self.translations.t('completed_tasks') if hasattr(self.translations, 't') else 'Completed Tasks:'}",
            font=("Roboto", 16)
        )
        self.done_tasks_label.pack(pady=5)
        
        self.overdue_tasks_label = ctk.CTkLabel(
            self,
            text=f"{self.translations.t('overdue_tasks') if hasattr(self.translations, 't') else 'Overdue Tasks:'}",
            font=("Roboto", 16)
        )
        self.overdue_tasks_label.pack(pady=5)
        
        self.total_projects_label = ctk.CTkLabel(
            self,
            text=f"{self.translations.t('total_projects') if hasattr(self.translations, 't') else 'Total Projects:'}",
            font=("Roboto", 16)
        )
        self.total_projects_label.pack(pady=5)

    def refresh(self) -> None:
        """
        Refreshes the dashboard data by recalculating task and project counts.
        """
        tasks = self.controller.list_tasks()
        total = len(tasks)
        done = len([t for t in tasks if t.done])
        overdue = 0  # Add overdue logic here as needed.
        projects = self.project_controller.list_projects()
        total_projects = len(projects)
        self.total_tasks_label.configure(text=f"{self.translations.t('total_tasks') if hasattr(self.translations, 't') else 'Total Tasks:'} {total}")
        self.done_tasks_label.configure(text=f"{self.translations.t('completed_tasks') if hasattr(self.translations, 't') else 'Completed Tasks:'} {done}")
        self.overdue_tasks_label.configure(text=f"{self.translations.t('overdue_tasks') if hasattr(self.translations, 't') else 'Overdue Tasks:'} {overdue}")
        self.total_projects_label.configure(text=f"{self.translations.t('total_projects') if hasattr(self.translations, 't') else 'Total Projects:'} {total_projects}")

"""
projects_view.py

ProjectsView displays all projects as cards arranged in a grid (3 per row).
Each card is clickable to open the project, and includes a delete button.
Inherits from BaseView for common functionality.
"""

import customtkinter as ctk
import theme
from controllers.project_controller import ProjectController
from models.project import Project
import tkinter.messagebox as messagebox
from controllers.task_controller import TaskController
from views.base_view import BaseView

class ProjectsView(BaseView):
    def __init__(self, master, navigate_project_callback, *args, **kwargs):
        """
        Initializes ProjectsView.

        Args:
            master: Parent widget.
            navigate_project_callback (callable): Function called with a project ID when a card is clicked.
            *args, **kwargs: Additional arguments.
        """
        super().__init__(master, *args, **kwargs)
        self.controller = ProjectController()
        self.navigate_project_callback = navigate_project_callback
        self._create_widgets()
        self.refresh()

    def _create_widgets(self):
        """
        Creates the header, scrollable project area, and add-project button.
        """
        self.title_label = ctk.CTkLabel(
            self,
            text=self.translations.t("projects"),
            font=theme.get_font("title")
        )
        self.title_label.pack(pady=10)

        # Scrollable container for project cards.
        self.projects_container = ctk.CTkScrollableFrame(self)
        self.projects_container.pack(pady=10, padx=10, fill="both", expand=True)

        # "Add Project" button.
        add_project_text = "+ " + (self.translations.t("add_project") if hasattr(self.translations, "t") else "Add Project")
        self.add_project_btn = ctk.CTkButton(
            self,
            text=add_project_text,
            fg_color=getattr(theme, "COLOR_PRIMARY", "#007BFF"),
            command=self._open_add_project_area
        )
        self.add_project_btn.pack(pady=10)

    def refresh(self) -> None:
        """
        Refresh the list of projects by clearing and repopulating the container.
        """
        for widget in self.projects_container.winfo_children():
            widget.destroy()
        projects = self.controller.list_projects()
        if not projects:
            no_proj_label = ctk.CTkLabel(
                self.projects_container,
                text=self.translations.t("no_projects") if hasattr(self.translations, "t") else "No projects yet. Click here to create one.",
                text_color="gray",
                anchor="center"
            )
            no_proj_label.grid(row=0, column=0, columnspan=3, pady=20)
            no_proj_label.bind("<Button-1>", lambda e: self._open_add_project_area())
        else:
            for idx, project in enumerate(projects):
                row = idx // 3
                col = idx % 3
                card = self._create_project_card(project)
                card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    def _create_project_card(self, project: Project):
        """
        Creates a card representing a project.
        The entire card (except the delete button) is clickable.

        Args:
            project (Project): The project model.
        Returns:
            ctk.CTkFrame: The project card widget.
        """
        card = ctk.CTkFrame(
            self.projects_container,
            fg_color="#3B3F45",
            corner_radius=10,
            border_width=1,
            border_color=theme.get_border_color() if hasattr(theme, "get_border_color") else "#FFFFFF",
            width=400,
            height=450
        )
        card.grid_propagate(False)
        
        def open_project(e=None):
            self.navigate_project_callback(project.id)
            
        # Bind click event to the entire card.
        card.bind("<Button-1>", open_project)
        
        title_label = ctk.CTkLabel(
            card,
            text=project.name,
            font=theme.get_font("title", size=24),
            text_color="white"
        )
        title_label.pack(pady=(20, 10), padx=10)
        title_label.bind("<Button-1>", open_project)
        
        # Display a shortened description.
        if project.description:
            short_desc = project.description if len(project.description) < 150 else project.description[:150] + "..."
        else:
            short_desc = self.translations.t("no_description") if hasattr(self.translations, "t") else "No description"
        desc_label = ctk.CTkLabel(
            card,
            text=short_desc,
            font=theme.get_font("text", size=18),
            text_color="gray",
            wraplength=380,
            justify="left"
        )
        desc_label.pack(pady=10, padx=10, fill="x")
        desc_label.bind("<Button-1>", open_project)
        
        # Delete button.
        delete_btn = ctk.CTkButton(
            card,
            text="X",
            fg_color="#FF6B6B",
            width=30,
            command=lambda: self._delete_project(project)
        )
        delete_btn.pack(pady=10)
        delete_btn.bind("<Button-1>", lambda e: ("break", delete_btn.invoke()))
        return card

    def _delete_project(self, project: Project):
        """
        Asks for confirmation and deletes the project.
        If the project has a description or associated tasks, additional confirmation is requested.

        Args:
            project (Project): The project model.
        """
        task_controller = TaskController()
        tasks = task_controller.list_tasks(project_id=project.id)
        if (project.description and project.description.strip()) or (tasks and len(tasks) > 0):
            choice = messagebox.askyesnocancel(
                self.translations.t("confirm_deletion") if hasattr(self.translations, "t") else "Confirm deletion",
                f"{self.translations.t('delete_project_msg') if hasattr(self.translations, 't') else 'Delete project and ALL associated tasks?'}\n"
                f"{self.translations.t('yes_delete_all') if hasattr(self.translations, 't') else 'Click Yes to delete project with its tasks.'}\n"
                f"{self.translations.t('no_keep_tasks') if hasattr(self.translations, 't') else 'Click No to delete project and KEEP tasks.'}\n"
                f"{self.translations.t('cancel') if hasattr(self.translations, 't') else 'Click Cancel to abort.'}"
            )
            if choice is None:
                return
            elif choice is True:
                self.controller.delete_project(project.id, delete_tasks=True)
            else:
                self.controller.delete_project(project.id, delete_tasks=False)
        else:
            self.controller.delete_project(project.id, delete_tasks=True)
        self.refresh()

    def _open_add_project_area(self):
        """
        Displays an inline form to create a new project.
        """
        if hasattr(self, "add_area") and self.add_area.winfo_exists():
            return
        row_count = self.projects_container.grid_size()[1]
        self.add_area = ctk.CTkFrame(
            self.projects_container,
            fg_color="#555555",
            corner_radius=10
        )
        self.add_area.grid(row=row_count, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")
        name_entry = ctk.CTkEntry(
            self.add_area,
            placeholder_text=self.translations.t("project_name") if hasattr(self.translations, "t") else "Project Name"
        )
        name_entry.pack(pady=5, padx=5, fill="x")
        desc_entry = ctk.CTkTextbox(self.add_area, height=60)
        desc_entry.pack(pady=5, padx=5, fill="x")
        name_entry.focus()
        create_btn = ctk.CTkButton(
            self.add_area,
            text=self.translations.t("create") if hasattr(self.translations, "t") else "Create",
            fg_color=getattr(theme, "COLOR_PRIMARY", "#007BFF"),
            command=lambda: save_project()
        )
        create_btn.pack(pady=5)
        
        def save_project(e=None):
            name = name_entry.get().strip()
            desc = desc_entry.get("0.0", "end").strip()
            if name:
                self.controller.create_project(name, desc)
            self.add_area.destroy()
            self.refresh()
            
        name_entry.bind("<Return>", save_project)

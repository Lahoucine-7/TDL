"""
tasks_view.py

TasksView is the primary view for displaying tasks in an interactive table.
It comprises:
  - A scrollable container to display the task table.
  - An "Add Task" button located at the bottom-right corner.

This view leverages a consistent style by using common fonts and colors from the theme.
"""

import customtkinter as ctk
from controllers.task_controller import TaskController
from utils.translations import TranslationsManager
from components.task_table import TaskTable
from theme import get_font
from views.base_view import BaseView  # Assuming you later extend TasksView from BaseView

class TasksView(BaseView):
    def __init__(self, master, *args, **kwargs):
        """
        Initialize TasksView.

        Args:
            master: The parent widget.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(master, *args, **kwargs)
        # Initialize controller and translation manager.
        self.controller = TaskController()
        self.translations = TranslationsManager(language="fr")
        
        # Dictionary to store filter/sort criteria.
        self.filter_sort_criteria = {}
        # Current project ID to filter tasks; set to None for all tasks.
        self.current_project = None

        # Configure grid to ensure view expands to fill the available space.
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._create_widgets()
        self.refresh_tasks()

    def _create_widgets(self):
        """
        Create and layout widgets used in the TasksView.
        """
        # Container frame for the task table; supports scrolling.
        self.table_container = ctk.CTkFrame(self)
        self.table_container.grid(row=1, column=0, sticky="nsew")
        self.table_container.grid_rowconfigure(0, weight=1)
        self.table_container.grid_columnconfigure(0, weight=1)

        # "Add Task" button positioned at the bottom-right.
        self.add_task_btn = ctk.CTkButton(
            self,
            text="+",
            font=get_font("title"),
            command=self._on_add_task,
            width=60,
            height=60,
            fg_color="#007BFF"
        )
        # Use place to position the button relative to the entire view.
        self.add_task_btn.place(relx=1, rely=1, anchor="se", x=-40, y=-40)

        # Placeholder label for when no tasks are present.
        self.empty_label = None

    def refresh_tasks(self):
        """
        Refresh the tasks list by clearing and re-populating the task table.
        If no tasks exist, displays a placeholder message.
        """
        # Clear any existing widgets in the container.
        for widget in self.table_container.winfo_children():
            widget.destroy()

        tasks = self.controller.list_tasks(project_id=self.current_project)
        if not tasks:
            # Show placeholder message when no tasks exist.
            if self.empty_label is None:
                self.empty_label = ctk.CTkLabel(
                    self.table_container,
                    text=self.translations.t("no_tasks") or "Click 'Add Task' to create one.",
                    text_color="gray",
                    font=get_font("button")
                )
                self.empty_label.pack(expand=True, fill="both", pady=20)
            return
        else:
            if self.empty_label:
                self.empty_label.destroy()
                self.empty_label = None

        # Create and add the task table widget.
        self.task_table = TaskTable(
            self.table_container,
            tasks=tasks,
            on_select_all=self._select_all_tasks,
            on_delete_selected=self._delete_selected_tasks,
            on_filter_sort_change=self._on_filter_sort_change,
            on_update=self._on_task_update,
            on_delete=self._on_task_delete,
            on_field_edit=self._on_field_edit,
            on_details_save=self._save_task_details,
            on_subtask_update=self._on_subtask_update
        )
        self.task_table.grid(row=0, column=0, sticky="nsew")

    def _select_all_tasks(self, selected):
        """
        Sets the selection state for all task rows.

        Args:
            selected (bool): True to select all tasks, False to deselect.
        """
        if hasattr(self, 'task_table'):
            for row in self.task_table.task_rows.values():
                row.select_var.set(selected)

    def _delete_selected_tasks(self):
        """
        Deletes tasks that have been selected.
        Prompts the user for confirmation before deleting.
        """
        selected_ids = []
        if hasattr(self, 'task_table'):
            for tid, row in self.task_table.task_rows.items():
                if row.select_var.get():
                    selected_ids.append(tid)
        if not selected_ids:
            return

        confirm = ctk.CTkToplevel(self)
        confirm.geometry("200x100")
        confirm.title("Confirm Deletion")
        msg = ctk.CTkLabel(confirm, text="Delete selected tasks?", font=get_font("button"))
        msg.pack(pady=10)
        btn_frame = ctk.CTkFrame(confirm)
        btn_frame.pack(pady=5)
        
        def confirm_delete():
            for tid in selected_ids:
                self.controller.delete_task(tid)
            confirm.destroy()
            self.refresh_tasks()
        
        ctk.CTkButton(btn_frame, text="Yes", command=confirm_delete, fg_color="#D9534F", font=get_font("button")).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="No", command=confirm.destroy, fg_color="gray", font=get_font("button")).pack(side="left", padx=5)

    def _on_filter_sort_change(self, field, value):
        """
        Updates the filter or sort criteria and refreshes the tasks view.

        Args:
            field (str): The field to filter or sort by.
            value: The new value for the criterion.
        """
        self.filter_sort_criteria[field] = value
        self.refresh_tasks()

    def _on_add_task(self):
        """
        Opens an inline entry field for creating a new task.
        Saves the task when the user presses Return or when the field loses focus.
        """
        entry_frame = ctk.CTkFrame(self.table_container, fg_color="#CCCCCC", corner_radius=5)
        entry_frame.pack(pady=5, padx=5, fill="x")
        entry = ctk.CTkEntry(entry_frame, placeholder_text="New Task Title", font=get_font("button"))
        entry.pack(side="left", padx=5, fill="x", expand=True)
        entry.focus()
        
        def save_entry(e=None):
            title = entry.get().strip()
            entry_frame.destroy()
            if title:
                self.controller.create_task(title=title, project_id=self.current_project)
            self.refresh_tasks()
        
        entry.bind("<Return>", save_entry)
        entry.bind("<FocusOut>", save_entry)

    def _on_task_update(self, task):
        """
        Callback triggered when a task is updated.
        
        Args:
            task: The updated task object.
        """
        self.refresh_tasks()

    def _on_task_delete(self, task_id):
        """
        Deletes a task and refreshes the view.

        Args:
            task_id (int): The ID of the task to delete.
        """
        self.controller.delete_task(task_id)
        self.refresh_tasks()

    def _save_task_details(self, task, new_values):
        """
        Updates task details with new values and refreshes the tasks view.

        Args:
            task: The task object to update.
            new_values (dict): A dictionary containing updated task fields.
        """
        if new_values.get("title", "").strip() == "":
            return
        task.description = new_values.get("description", task.description)
        task.due_date = new_values.get("due_date", task.due_date)
        task.time = new_values.get("time", task.time)
        try:
            task.duration = int(new_values.get("duration", task.duration))
        except ValueError:
            task.duration = task.duration
        self.controller.update_task(task)
        self.refresh_tasks()

    def _on_field_edit(self, field, new_value, task):
        """
        Updates a specific field of a task after in-line editing.

        Args:
            field (str): The field being edited (e.g., "title", "status").
            new_value: The new value for the field.
            task: The task object to update.
        """
        if field == "title":
            if new_value.strip() == "":
                return
            task.title = new_value
        elif field == "project":
            task.project = new_value
        elif field == "status":
            task.status = new_value
        elif field == "priority":
            task.priority = new_value
        elif field == "due_date":
            task.due_date = new_value
        elif field == "updated_at":
            task.updated_at = new_value
        self.controller.update_task(task)
        self.refresh_tasks()

    def _on_subtask_update(self, action, data):
        """
        Placeholder for handling subtask updates.

        Args:
            action: The action to perform on the subtask.
            data: Additional data for the subtask update.
        """
        # Implement subtask update functionality as needed.
        pass

    def set_project(self, project_id):
        """
        Filters displayed tasks based on the selected project.

        Args:
            project_id (int): The project ID to filter by.
        """
        self.current_project = project_id
        self.refresh_tasks()

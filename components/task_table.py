"""
task_table.py

TaskTable combines the header and task rows into a unified table-like component.
It displays a fixed-height header with sorting and filtering controls,
and a scrollable area containing individual TaskRow components.
"""

import customtkinter as ctk
from components.tasks_table_header import TasksTableHeader, HEADER_HEIGHT
from components.task_row import TaskRow
from theme import get_font

class TaskTable(ctk.CTkFrame):
    def __init__(self, master, tasks, on_select_all, on_delete_selected, on_filter_sort_change, 
                 on_update, on_delete, on_field_edit, on_details_save, on_subtask_update, **kwargs):
        """
        Initialize TaskTable.

        Args:
            master: Parent widget.
            tasks (list): List of Task objects.
            on_select_all (callable): Callback for selecting/deselecting all tasks.
            on_delete_selected (callable): Callback to delete selected tasks.
            on_filter_sort_change (callable): Callback for filtering/sorting.
            on_update (callable): Callback when a task is updated.
            on_delete (callable): Callback when a task is deleted.
            on_field_edit (callable): Callback for inline field editing.
            on_details_save (callable): Callback for saving task details.
            on_subtask_update (callable): Callback to manage subtask updates.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(master, **kwargs)
        self.tasks = tasks
        self.on_select_all = on_select_all
        self.on_delete_selected = on_delete_selected
        self.on_filter_sort_change = on_filter_sort_change
        self.on_update = on_update
        self.on_delete = on_delete
        self.on_field_edit = on_field_edit
        self.on_details_save = on_details_save
        self.on_subtask_update = on_subtask_update
        self.task_rows = {}  # Dictionary to hold TaskRow instances.
        self._create_widgets()

    def _create_widgets(self):
        """
        Configures the grid layout and creates the header and rows container.
        """
        # Configure grid rows: header row is fixed; rows container expands.
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create the header component.
        self.header = TasksTableHeader(
            self,
            on_select_all=self.on_select_all,
            on_delete_selected=self.on_delete_selected,
            on_filter_sort_change=self.on_filter_sort_change
        )
        self.header.configure(height=HEADER_HEIGHT)
        self.header.grid(row=0, column=0, sticky="ew")
        self.header.grid_propagate(False)  # Maintain fixed header height.
        
        # Create container for task rows.
        self.rows_container = ctk.CTkFrame(self)
        self.rows_container.grid(row=1, column=0, sticky="nsew")
        self.rows_container.grid_columnconfigure(0, weight=1)
        
        self._create_task_rows()

    def _create_task_rows(self):
        """
        Clears and repopulates the rows container with TaskRow widgets.
        """
        for widget in self.rows_container.winfo_children():
            widget.destroy()
        self.task_rows = {}
        row_index = 0
        for task in self.tasks:
            task_row = TaskRow(
                self.rows_container,
                task=task,
                on_update=self.on_update,
                on_delete=self.on_delete,
                on_toggle_details=lambda task=task: self._toggle_row_details(task),
                on_field_edit=self.on_field_edit,
                on_details_save=self.on_details_save,
                on_subtask_update=self.on_subtask_update
            )
            # Each row spans full width with some padding.
            task_row.grid(row=row_index, column=0, sticky="ew", padx=5, pady=3)
            self.task_rows[task.id] = task_row
            row_index += 1

    def refresh(self, tasks):
        """
        Refreshes the entire task table with an updated list of tasks.

        Args:
            tasks (list): Updated list of Task objects.
        """
        self.tasks = tasks
        self._create_task_rows()

    def _toggle_row_details(self, task):
        """
        Toggles the detailed view for a specific task row.

        Args:
            task (Task): The task for which details should be toggled.
        """
        if task.id in self.task_rows:
            self.task_rows[task.id].toggle_details()

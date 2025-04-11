"""
task_details.py

TaskDetails is a component for displaying and editing detailed information about a task,
including the description, due date, time, duration, and managing subtasks.

It presents a comprehensive form that allows users to modify task details and update
subtasks through associated callbacks.
"""

import customtkinter as ctk
from tkcalendar import DateEntry
from theme import get_font

class TaskDetails(ctk.CTkFrame):
    def __init__(self, master, task, on_save, on_subtask_update, *args, **kwargs):
        """
        Initialize the TaskDetails component.

        Args:
            master: The parent widget.
            task (Task): The task instance whose details will be shown and edited.
            on_save (callable): Callback triggered when saving the updated details.
                                Should accept the task and a dictionary of updated values.
            on_subtask_update (callable): Callback to handle adding, removing, or updating subtasks.
            *args, **kwargs: Additional arguments.
        """
        super().__init__(master, *args, **kwargs)
        self.task = task
        self.on_save = on_save
        self.on_subtask_update = on_subtask_update
        self._create_widgets()

    def _create_widgets(self):
        """
        Create and configure all widgets for editing task details.
        """
        self.columnconfigure(1, weight=1)
        row = 0

        # Task Description
        desc_label = ctk.CTkLabel(self, text="Description:", font=get_font("button"))
        desc_label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
        self.desc_text = ctk.CTkTextbox(self, width=250, height=60, font=get_font("text"))
        self.desc_text.insert("0.0", self.task.description or "")
        self.desc_text.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        row += 1

        # Due Date Field
        date_label = ctk.CTkLabel(self, text="Due Date:", font=get_font("button"))
        date_label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
        self.date_entry = DateEntry(self, date_pattern="yyyy-mm-dd")
        if self.task.due_date:
            self.date_entry.set_date(self.task.due_date)
        self.date_entry.grid(row=row, column=1, sticky="w", padx=5, pady=5)
        row += 1

        # Time Field
        time_label = ctk.CTkLabel(self, text="Time:", font=get_font("button"))
        time_label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
        self.time_entry = ctk.CTkEntry(self, font=get_font("button"))
        self.time_entry.insert(0, self.task.time or "")
        self.time_entry.grid(row=row, column=1, sticky="w", padx=5, pady=5)
        row += 1

        # Duration Field
        duration_label = ctk.CTkLabel(self, text="Duration (min):", font=get_font("button"))
        duration_label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
        self.duration_entry = ctk.CTkEntry(self, font=get_font("button"))
        self.duration_entry.insert(0, str(self.task.duration) if self.task.duration else "")
        self.duration_entry.grid(row=row, column=1, sticky="w", padx=5, pady=5)
        row += 1

        # Save Button
        save_btn = ctk.CTkButton(self, text="Save", font=get_font("button"), command=self._save_details)
        save_btn.grid(row=row, column=0, columnspan=2, pady=10)
        row += 1

        # Subtasks Section
        sub_label = ctk.CTkLabel(self, text="Subtasks:", font=get_font("button"))
        sub_label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
        self.subtask_frame = ctk.CTkFrame(self)
        self.subtask_frame.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        self._populate_subtasks()

    def _populate_subtasks(self):
        """
        Populate the subtasks area with existing subtasks and a field to add new ones.
        """
        # Clear existing subtask widgets.
        for widget in self.subtask_frame.winfo_children():
            widget.destroy()
        row = 0
        # Create an entry and delete button for each existing subtask.
        for sub in self.task.subtasks:
            sub_entry = ctk.CTkEntry(self.subtask_frame, font=get_font("text"))
            sub_entry.insert(0, sub.title)
            sub_entry.grid(row=row, column=0, padx=5, pady=2, sticky="ew")
            del_btn = ctk.CTkButton(self.subtask_frame, text="X", width=25, fg_color="#D9534F",
                                    command=lambda s=sub: self.on_subtask_update("delete", s))
            del_btn.grid(row=row, column=1, padx=5, pady=2)
            row += 1
        # Field for adding a new subtask.
        self.new_sub_entry = ctk.CTkEntry(self.subtask_frame, placeholder_text="Add subtask", font=get_font("text"))
        self.new_sub_entry.grid(row=row, column=0, padx=5, pady=5, sticky="ew")
        add_btn = ctk.CTkButton(self.subtask_frame, text="+", width=25, fg_color="#007BFF",
                                command=lambda: self.on_subtask_update("add", self.new_sub_entry.get()))
        add_btn.grid(row=row, column=1, padx=5, pady=5)

    def _save_details(self):
        """
        Gathers details from the form and calls the on_save callback.
        """
        details = {
            "description": self.desc_text.get("0.0", "end").strip(),
            "due_date": self.date_entry.get(),
            "time": self.time_entry.get().strip(),
            "duration": self.duration_entry.get().strip()
        }
        self.on_save(self.task, details)

"""
task_row.py

TaskRow represents a single row in the task table, showing task details such as title,
project, status, priority, due date, and last update. It also provides inline editing features
and a toggle for displaying additional details.

It uses a common grid configuration from grid_config.py for consistent column layouts.
"""

import customtkinter as ctk
from theme import get_font
from components.task_details import TaskDetails
from datetime import datetime, date
from tkcalendar import DateEntry
from components.grid_config import COMMON_GRID_CONFIG

SEPARATOR_COLOR = "#CCCCCC"

class TaskRow(ctk.CTkFrame):
    def __init__(self, master, task, on_update, on_delete, on_toggle_details, on_field_edit, on_details_save, on_subtask_update):
        """
        Initialize a TaskRow.

        Args:
            master: Parent container.
            task (Task): The task instance to represent.
            on_update (callable): Callback to invoke when the task is updated.
            on_delete (callable): Callback to invoke when deleting the task.
            on_toggle_details (callable): Callback to toggle the detailed view.
            on_field_edit (callable): Callback to handle inline field edits.
            on_details_save (callable): Callback to save updated task details.
            on_subtask_update (callable): Callback to handle subtask updates.
        """
        super().__init__(master)
        self.task = task
        self.on_update = on_update
        self.on_delete = on_delete
        self.on_toggle_details = on_toggle_details
        self.on_field_edit = on_field_edit
        self.on_details_save = on_details_save
        self.on_subtask_update = on_subtask_update
        self.details_shown = False
        self.due_date_editor = None

        # Variables for inline editing.
        self.select_var = ctk.BooleanVar(value=False)
        self.title_var = ctk.StringVar(value=self.task.title)
        self.project_var = ctk.StringVar(value=getattr(self.task, "project", "None"))
        self.status_var = ctk.StringVar(value=getattr(self.task, "status", "Not Started"))
        self.priority_var = ctk.StringVar(value=getattr(self.task, "priority", "Medium"))
        self.duedate_var = ctk.StringVar(value=self._format_date(self.task.due_date, default_today=True))
        self.updated_var = ctk.StringVar(value=self._format_date(self.task.updated_at, modifiable=False))
        
        # Apply common grid configuration.
        for col, conf in COMMON_GRID_CONFIG.items():
            self.grid_columnconfigure(col, **conf)
        
        self._create_widgets()

    def _format_date(self, date_str, default_today=False, modifiable=True) -> str:
        """
        Formats an ISO date string into a display format.

        Args:
            date_str (str): The ISO date string.
            default_today (bool): If True and date_str is empty, use today's date.
            modifiable (bool): Flag indicating if field is modifiable.
        
        Returns:
            str: Formatted date string.
        """
        if not date_str:
            if default_today:
                dt = datetime.combine(date.today(), datetime.strptime("00:00", "%H:%M").time())
            else:
                return ""
        else:
            try:
                dt = datetime.fromisoformat(date_str)
            except Exception:
                return date_str
        return dt.strftime("%d/%m - %H:%M")

    def _vertical_separator(self):
        """
        Creates a vertical separator widget.

        Returns:
            CTkFrame: A small frame used as a separator.
        """
        return ctk.CTkFrame(self, width=COMMON_GRID_CONFIG[1]["minsize"], height=20, fg_color=SEPARATOR_COLOR, bg_color=SEPARATOR_COLOR)

    def _create_widgets(self):
        """
        Creates and places all widgets for the task row.
        """
        # Checkbox for selection.
        self.checkbox = ctk.CTkCheckBox(self, variable=self.select_var, text="", width=30)
        self.checkbox.grid(row=0, column=0, padx=(3,0), pady=3, sticky="nsew")

        # Separator.
        sep1 = self._vertical_separator()
        sep1.grid(row=0, column=1, padx=2, pady=3)

        # Title label (clickable to enter edit mode).
        self.title_label = ctk.CTkLabel(self, textvariable=self.title_var, anchor="w", font=get_font("button"))
        self.title_label.grid(row=0, column=2, padx=3, pady=3, sticky="nsew")
        self.title_label.bind("<Button-1>", lambda e: self._enter_edit_mode("title"))

        # Separator.
        sep2 = self._vertical_separator()
        sep2.grid(row=0, column=3, padx=2, pady=3)

        # Project label.
        self.project_label = ctk.CTkLabel(self, textvariable=self.project_var, anchor="w", font=get_font("button"))
        self.project_label.grid(row=0, column=4, padx=3, pady=3, sticky="nsew")
        self.project_label.bind("<Button-1>", lambda e: self._enter_edit_mode("project"))

        # Separator.
        sep3 = self._vertical_separator()
        sep3.grid(row=0, column=5, padx=2, pady=3)

        # Status label.
        self.status_label = ctk.CTkLabel(self, textvariable=self.status_var, anchor="w", font=get_font("button"))
        self.status_label.grid(row=0, column=6, padx=3, pady=3, sticky="nsew")
        self.status_label.bind("<Button-1>", lambda e: self._enter_edit_mode("status"))

        # Separator.
        sep4 = self._vertical_separator()
        sep4.grid(row=0, column=7, padx=2, pady=3)

        # Priority label.
        self.priority_label = ctk.CTkLabel(self, textvariable=self.priority_var, anchor="w", font=get_font("button"))
        self.priority_label.grid(row=0, column=8, padx=3, pady=3, sticky="nsew")
        self.priority_label.bind("<Button-1>", lambda e: self._enter_edit_mode("priority"))

        # Separator.
        sep5 = self._vertical_separator()
        sep5.grid(row=0, column=9, padx=2, pady=3)

        # Due date label.
        self.duedate_label = ctk.CTkLabel(self, textvariable=self.duedate_var, anchor="w", font=get_font("button", size=10))
        self.duedate_label.grid(row=0, column=10, padx=3, pady=3, sticky="nsew")
        self.duedate_label.bind("<Button-1>", lambda e: self._enter_edit_mode("due_date"))

        # Separator.
        sep6 = self._vertical_separator()
        sep6.grid(row=0, column=11, padx=2, pady=3)

        # Last update label.
        self.updated_label = ctk.CTkLabel(self, textvariable=self.updated_var, anchor="w", font=get_font("button", size=10))
        self.updated_label.grid(row=0, column=12, padx=3, pady=3, sticky="nsew")

        # Toggle details button.
        self.toggle_btn = ctk.CTkButton(self, text="▼", width=30, command=self.toggle_details)
        self.toggle_btn.grid(row=0, column=13, padx=3, pady=3, sticky="nsew")

        # Delete task button.
        self.delete_btn = ctk.CTkButton(self, text="X", width=30, fg_color="#D9534F", command=self._confirm_delete)
        self.delete_btn.grid(row=0, column=14, padx=3, pady=3, sticky="nsew")

    def _enter_edit_mode(self, field):
        """
        Enters inline edit mode for the specified field.

        Args:
            field (str): The field to edit ("title", "project", "status", "priority", "due_date").
        """
        if field == "title":
            entry = ctk.CTkEntry(self, textvariable=self.title_var, font=get_font("button"))
            entry.grid(row=0, column=2, padx=3, pady=3, sticky="ew")
            entry.focus()
            entry.bind("<Return>", lambda e: self._save_field("title", entry.get(), entry))
            entry.bind("<FocusOut>", lambda e: self._save_field("title", entry.get(), entry))
        elif field == "project":
            # Here you may open an option menu to choose a project.
            project_options = self._get_project_list()
            option_menu = ctk.CTkOptionMenu(self, values=project_options, font=get_font("button"),
                                            command=lambda v: self._save_option("project", v))
            option_menu.set(self.project_var.get())
            option_menu.grid(row=0, column=4, padx=3, pady=3, sticky="ew")
        elif field == "status":
            status_options = ["Not Started", "In Progress", "Completed"]
            option_menu = ctk.CTkOptionMenu(self, values=status_options, font=get_font("button"),
                                            command=lambda v: self._save_option("status", v))
            option_menu.set(self.status_var.get())
            option_menu.grid(row=0, column=6, padx=3, pady=3, sticky="ew")
        elif field == "priority":
            priority_options = ["Low", "Medium", "High"]
            option_menu = ctk.CTkOptionMenu(self, values=priority_options, font=get_font("button"),
                                            command=lambda v: self._save_option("priority", v))
            option_menu.set(self.priority_var.get())
            option_menu.grid(row=0, column=8, padx=3, pady=3, sticky="ew")
        elif field == "due_date":
            if self.due_date_editor is not None:
                return
            if self.details_shown:
                self.toggle_details()
            self._open_inline_due_date_editor()

    def _save_option(self, field, value):
        """
        Saves a new option value for a specified field and triggers callbacks.

        Args:
            field (str): The field being edited.
            value (str): The new value.
        """
        if field == "project":
            self.project_var.set(value)
        elif field == "status":
            self.status_var.set(value)
        elif field == "priority":
            self.priority_var.set(value)
        self.on_field_edit(field, value, self.task)
        self.on_update(self.task)

    def _get_project_list(self):
        """
        Retrieves a list of project names.
        (Replace this placeholder with a call to your project controller, if available.)

        Returns:
            list: List of project name strings.
        """
        projects = ["Project A", "Project B", "Project C"]
        return projects if projects else ["-------"]

    def _open_inline_due_date_editor(self):
        """
        Opens an inline editor to update the due date.
        """
        self.due_date_editor = ctk.CTkFrame(self)
        self.due_date_editor.grid(row=1, column=10, columnspan=3, sticky="ew", pady=(0,3))
        self.due_date_editor.columnconfigure(0, weight=1)

        self.date_entry = DateEntry(self.due_date_editor, date_pattern="dd/mm/yyyy")
        try:
            current_dt = datetime.strptime(self.duedate_var.get(), "%d/%m - %H:%M")
        except Exception:
            current_dt = datetime.now()
        self.date_entry.set_date(current_dt.date())
        self.date_entry.grid(row=0, column=0, padx=3, pady=2, sticky="ew")
        self.date_entry.bind("<<DateEntrySelected>>", lambda e: self._save_inline_due_date())

        self.hour_entry = ctk.CTkEntry(self.due_date_editor, width=30, font=get_font("button", size=10), placeholder_text="HH")
        self.hour_entry.insert(0, current_dt.strftime("%H"))
        self.hour_entry.grid(row=0, column=1, padx=2, pady=2)
        self.hour_entry.bind("<FocusOut>", lambda e: self._save_inline_due_date())
        self.hour_entry.bind("<Return>", lambda e: self._save_inline_due_date())

        self.minute_entry = ctk.CTkEntry(self.due_date_editor, width=30, font=get_font("button", size=10), placeholder_text="MM")
        self.minute_entry.insert(0, current_dt.strftime("%M"))
        self.minute_entry.grid(row=0, column=2, padx=2, pady=2)
        self.minute_entry.bind("<FocusOut>", lambda e: self._save_inline_due_date())
        self.minute_entry.bind("<Return>", lambda e: self._save_inline_due_date())

    def _save_inline_due_date(self):
        """
        Saves the inline edited due date value and triggers callbacks.
        """
        selected_date = self.date_entry.get_date()
        try:
            hour = int(self.hour_entry.get())
            if not (0 <= hour < 24):
                hour = 0
        except Exception:
            hour = 0
        try:
            minute = int(self.minute_entry.get())
            if not (0 <= minute < 60):
                minute = 0
        except Exception:
            minute = 0
        dt = datetime.combine(selected_date, datetime.strptime(f"{hour:02d}:{minute:02d}", "%H:%M").time())
        formatted = dt.strftime("%d/%m - %H:%M")
        self.duedate_var.set(formatted)
        self.on_field_edit("due_date", formatted, self.task)
        self.on_update(self.task)
        if self.due_date_editor is not None:
            self.due_date_editor.destroy()
            self.due_date_editor = None

    def _save_field(self, field, new_value, entry_widget):
        """
        Saves the edited value for a given field upon exiting edit mode.

        Args:
            field (str): Field being edited.
            new_value (str): New value entered.
            entry_widget: The widget used for editing.
        """
        if field == "title" and new_value.strip() == "":
            entry_widget.configure(border_color="red")
            self.after(500, lambda: entry_widget.configure(border_color="transparent"))
            return
        self.on_field_edit(field, new_value, self.task)
        self.on_update(self.task)

    def _confirm_delete(self):
        """
        Displays an inline confirmation for deletion.
        """
        confirm_frame = ctk.CTkFrame(self, fg_color="red", corner_radius=5)
        confirm_frame.grid(row=0, column=15, padx=5)
        confirm_label = ctk.CTkLabel(confirm_frame, text="Delete?", font=get_font("button"), text_color="white")
        confirm_label.grid(row=0, column=0, padx=5, pady=5)
        yes_btn = ctk.CTkButton(confirm_frame, text="Yes", width=30, fg_color="red",
                                 command=lambda: [self.on_delete(self.task.id), confirm_frame.destroy()])
        yes_btn.grid(row=0, column=1, padx=5, pady=5)
        no_btn = ctk.CTkButton(confirm_frame, text="No", width=30, fg_color="gray",
                                command=lambda: confirm_frame.destroy())
        no_btn.grid(row=0, column=2, padx=5, pady=5)

    def toggle_details(self):
        """
        Toggles the display of task details.
        """
        if not self.details_shown:
            if self.due_date_editor is not None:
                self.due_date_editor.destroy()
                self.due_date_editor = None
            self.details_frame = TaskDetails(
                self,
                task=self.task,
                on_save=self.on_details_save,
                on_subtask_update=self.on_subtask_update
            )
            self.details_frame.grid(row=1, column=0, columnspan=15, sticky="ew", pady=5, padx=5)
            self.toggle_btn.configure(text="▲")
            self.details_shown = True
        else:
            if self.details_frame:
                self.details_frame.grid_forget()
            self.toggle_btn.configure(text="▼")
            self.details_shown = False

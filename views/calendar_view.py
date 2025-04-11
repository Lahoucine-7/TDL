"""
calendar_view.py

CalendarView displays a calendar and lists tasks corresponding to the selected date.
Inherits from BaseView to benefit from consistent theme and translation management.
"""

import customtkinter as ctk
from tkcalendar import Calendar
from controllers.task_controller import TaskController
from views.base_view import BaseView

class CalendarView(BaseView):
    def __init__(self, master, *args, **kwargs):
        """
        Initializes CalendarView.

        Args:
            master: Parent widget.
            *args, **kwargs: Additional arguments.
        """
        super().__init__(master, *args, **kwargs)
        self.controller = TaskController()
        self._create_widgets()

    def _create_widgets(self):
        """
        Creates and places widgets for the calendar view.
        """
        # Title label using translation.
        self.title_label = ctk.CTkLabel(
            self,
            text=self.translations.t("calendar"),
            font=("Roboto", 20)
        )
        self.title_label.pack(pady=10)

        # Calendar widget for date selection.
        self.calendar = Calendar(self, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendar.pack(pady=10)

        # Button to show tasks.
        show_tasks_text = self.translations.t("show_tasks") if hasattr(self.translations, "t") else "Show Tasks"
        self.show_tasks_button = ctk.CTkButton(
            self,
            text=show_tasks_text,
            command=self._show_tasks
        )
        self.show_tasks_button.pack(pady=10)

        # Textbox to display tasks.
        self.tasks_textbox = ctk.CTkTextbox(self, width=600, height=300)
        self.tasks_textbox.pack(pady=10)

    def _show_tasks(self):
        """
        Retrieves and displays tasks corresponding to the selected date.
        """
        self.tasks_textbox.delete("1.0", "end")
        selected_date = self.calendar.get_date()
        try:
            all_tasks = self.controller.list_tasks()
            tasks_for_date = [t for t in all_tasks if t.due_date == selected_date]
            if tasks_for_date:
                for t in tasks_for_date:
                    self.tasks_textbox.insert("end", f"{t}\n")
                    for sub in t.subtasks:
                        self.tasks_textbox.insert("end", f"   -> {sub}\n")
                    self.tasks_textbox.insert("end", "\n")
            else:
                msg = self.translations.t("no_tasks_for_date") if hasattr(self.translations, "t") else "No tasks for this date."
                self.tasks_textbox.insert("end", msg)
        except Exception as e:
            self.tasks_textbox.insert("end", f"Error: {e}")

    def refresh(self) -> None:
        """
        Refresh the calendar view content.
        Simply re-run the _show_tasks method to update displayed tasks.
        """
        self._show_tasks()

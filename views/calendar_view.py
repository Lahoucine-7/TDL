# views/calendar_view.py

import customtkinter as ctk
from tkcalendar import Calendar
from controllers.task_controller import TaskController

class CalendarView(ctk.CTkFrame):
    """
    Vue affichant un calendrier et les tâches pour la date sélectionnée.
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.controller = TaskController()
        self._create_widgets()

    def _create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="Calendar View", font=("Roboto", 20))
        self.title_label.pack(pady=10)
        self.calendar = Calendar(self, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendar.pack(pady=10)
        self.show_tasks_button = ctk.CTkButton(self, text="Show Tasks", command=self._show_tasks)
        self.show_tasks_button.pack(pady=10)
        self.tasks_textbox = ctk.CTkTextbox(self, width=600, height=300)
        self.tasks_textbox.pack(pady=10)

    def _show_tasks(self):
        self.tasks_textbox.delete("1.0", "end")
        selected_date = self.calendar.get_date()
        try:
            all_tasks = self.controller.list_tasks()
            tasks_for_date = [t for t in all_tasks if t.date == selected_date]
            if tasks_for_date:
                for t in tasks_for_date:
                    self.tasks_textbox.insert("end", f"{t}\n")
                    for sub in t.subtasks:
                        self.tasks_textbox.insert("end", f"   -> {sub}\n")
                    self.tasks_textbox.insert("end", "\n")
            else:
                self.tasks_textbox.insert("end", "No tasks for this date.")
        except Exception as e:
            self.tasks_textbox.insert("end", f"Error: {e}")

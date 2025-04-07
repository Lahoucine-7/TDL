import customtkinter as ctk
from tkcalendar import Calendar
from controllers.task_controller import list_tasks

class CalendarView(ctk.CTkFrame):
    """View displaying a calendar and tasks for a selected date."""
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="Task Calendar", font=("Helvetica", 20))
        self.title_label.pack(pady=10)

        self.calendar = Calendar(self, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendar.pack(pady=10)

        self.show_tasks_button = ctk.CTkButton(self, text="Show Tasks", command=self.show_tasks)
        self.show_tasks_button.pack(pady=10)

        self.tasks_textbox = ctk.CTkTextbox(self, width=600, height=300)
        self.tasks_textbox.pack(pady=10)

    def show_tasks(self):
        """Display tasks corresponding to the selected date."""
        self.tasks_textbox.delete("1.0", "end")
        selected_date = self.calendar.get_date()
        all_tasks = list_tasks()
        filtered_tasks = [task for task in all_tasks if task.date == selected_date]
        if filtered_tasks:
            for task in filtered_tasks:
                self.tasks_textbox.insert("end", f"{task}\n")
                if task.subtasks:
                    for sub in task.subtasks:
                        self.tasks_textbox.insert("end", f"   -> {sub}\n")
                self.tasks_textbox.insert("end", "\n")
        else:
            self.tasks_textbox.insert("end", "No tasks for this date.")

# views/calendar_view.py

import customtkinter as ctk
from tkcalendar import Calendar
from controllers.task_controller import lister_taches

class CalendarView(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        # Titre de la vue
        self.label = ctk.CTkLabel(self, text="Calendrier des tâches", font=("Helvetica", 20))
        self.label.pack(pady=10)
        
        # Widget calendrier
        self.calendar = Calendar(self, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendar.pack(pady=10)
        
        # Bouton pour afficher les tâches de la date sélectionnée
        self.show_tasks_button = ctk.CTkButton(self, text="Afficher les tâches", command=self.show_tasks)
        self.show_tasks_button.pack(pady=10)
        
        # Zone de texte pour afficher les tâches
        self.task_text = ctk.CTkTextbox(self, width=600, height=300)
        self.task_text.pack(pady=10)

    def show_tasks(self):
        # Effacer l'affichage actuel
        self.task_text.delete("1.0", "end")
        # Récupérer la date sélectionnée (format : yyyy-mm-dd)
        selected_date = self.calendar.get_date()
        # Récupérer toutes les tâches
        all_tasks = lister_taches()
        # Filtrer les tâches correspondant à la date sélectionnée
        filtered_tasks = [t for t in all_tasks if t.date == selected_date]
        if filtered_tasks:
            for task in filtered_tasks:
                self.task_text.insert("end", f"{task}\n")
                if task.subtasks:
                    for sub in task.subtasks:
                        self.task_text.insert("end", f"   -> {sub}\n")
                self.task_text.insert("end", "\n")
        else:
            self.task_text.insert("end", "Aucune tâche pour cette date.")

import customtkinter as ctk
from views.main_view import MainView
from views.calendar_view import CalendarView
from views.settings_view import SettingsView

class TodoApp(ctk.CTk):

    themes_mode = ["dark", "light"]

    def __init__(self):
        super().__init__()

        self.title("Advanced To-Do List")
        self.geometry("1000x600")

        
        self.current_mode = self.themes_mode[0]

        # Configuration thèmes (clair/sombre)
        ctk.set_appearance_mode(self.current_mode)  # dark / light
        ctk.set_default_color_theme("blue")

        # Créer une barre latérale
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")

        # Créer la zone principale pour les vues et la configurer avec grid
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(side="right", expand=True, fill="both")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Créer les vues sans les packer, mais en les plaçant via grid
        self.main_view = MainView(self.main_frame)
        self.calendar_view = CalendarView(self.main_frame)
        self.settings_view = SettingsView(self.main_frame, self.toggle_theme)

        # Placer toutes les vues dans la même cellule
        self.main_view.grid(row=0, column=0, sticky="nsew")
        self.calendar_view.grid(row=0, column=0, sticky="nsew")
        self.settings_view.grid(row=0, column=0, sticky="nsew")

        # Afficher la vue principale par défaut
        self.show_view(self.main_view)

        # Ajouter boutons dans la barre latérale
        self.add_sidebar_buttons()

    def add_sidebar_buttons(self):
        btn_todo = ctk.CTkButton(self.sidebar_frame, text="Mes Tâches", command=lambda: self.show_view(self.main_view))
        btn_calendar = ctk.CTkButton(self.sidebar_frame, text="Calendrier", command=lambda: self.show_view(self.calendar_view))
        btn_settings = ctk.CTkButton(self.sidebar_frame, text="Paramètres", command=lambda: self.show_view(self.settings_view))

        btn_todo.pack(pady=10, padx=10)
        btn_calendar.pack(pady=10, padx=10)
        btn_settings.pack(pady=10, padx=10)

    def show_view(self, view):
        view.tkraise()

    def toggle_theme(self):
        self.current_mode = self.themes_mode[1] if self.current_mode == self.themes_mode[0] else self.themes_mode[0]
        ctk.set_appearance_mode(self.current_mode)

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()

# app.py

import customtkinter as ctk
from data.database import init_db
from views.main_view import MainView
from views.calendar_view import CalendarView
from views.settings_view import SettingsView

def run_app():
    """
    Point d'entrée pour exécuter la ToDoApp.
    - Initialise la base de données
    - Instancie et lance la fenêtre principale
    """
    try:
        init_db()  # Initialisation DB (peut lever une exception)
    except Exception as e:
        print(f"[Erreur] Impossible d'initialiser la base de données : {e}")

    app = TodoApp()
    app.mainloop()

class TodoApp(ctk.CTk):
    """
    Fenêtre principale de l'application.
    Gère la barre latérale de navigation et le chargement des vues.
    """
    THEMES = ["dark", "light"]

    def __init__(self):
        super().__init__()
        self.title("Advanced To-Do List")
        self.geometry("1080x720")

        # Thème par défaut
        self.current_theme = self.THEMES[0]
        ctk.set_appearance_mode(self.current_theme)
        ctk.set_default_color_theme("blue")

        # Barre latérale
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")

        # Conteneur principal des vues
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(side="right", expand=True, fill="both")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Création des différentes vues
        self.main_view = MainView(self.main_frame)
        self.calendar_view = CalendarView(self.main_frame)
        self.settings_view = SettingsView(self.main_frame, self.toggle_theme)

        # On les place toutes dans la même cellule (row=0, col=0)
        for view in (self.main_view, self.calendar_view, self.settings_view):
            view.grid(row=0, column=0, sticky="nsew")

        # On affiche la vue principale par défaut
        self.show_view(self.main_view)

        # Boutons de navigation
        self._create_sidebar_buttons()

    def _create_sidebar_buttons(self):
        """Création des boutons de la barre latérale."""
        btn_tasks = ctk.CTkButton(self.sidebar_frame, text="Tasks",
                                  command=lambda: self.show_view(self.main_view))
        btn_calendar = ctk.CTkButton(self.sidebar_frame, text="Calendar",
                                     command=lambda: self.show_view(self.calendar_view))
        btn_settings = ctk.CTkButton(self.sidebar_frame, text="Settings",
                                     command=lambda: self.show_view(self.settings_view))

        btn_tasks.pack(pady=10, padx=10)
        btn_calendar.pack(pady=10, padx=10)
        btn_settings.pack(pady=10, padx=10)

    def show_view(self, view):
        """Amène la vue spécifiée au premier plan (tkraise)."""
        view.tkraise()

    def toggle_theme(self):
        """Bascule entre le mode sombre et clair."""
        self.current_theme = (
            self.THEMES[1] if self.current_theme == self.THEMES[0] else self.THEMES[0]
        )
        ctk.set_appearance_mode(self.current_theme)

        # Optionnel: replacer le focus sur le conteneur principal
        try:
            self.main_frame.focus_set()
        except Exception as e:
            print("Error setting focus:", e)

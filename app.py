import logging
import customtkinter as ctk
import theme

from database.database import init_db
from views.main_view import MainView
from views.calendar_view import CalendarView
from views.dashboard_view import DashboardView
from views.settings_view import SettingsView
from views.projects_view import ProjectsView
from views.sidebar import Sidebar
from views.header import Header
from utils.translations import TranslationsManager

# Configuration basique du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
translations = TranslationsManager(language="fr")

# Titres traduits pour les vues de l'application
VIEW_TITLES = {
    "dashboard": translations.t("dashboard"),
    "calendar": translations.t("calendar"),
    "tasks": translations.t("tasks"),
    "projects": translations.t("projects"),
    "settings": translations.t("settings"),
    "project": translations.t("project")
}

def run_app():
    """Initialise la base de données et lance l'application."""
    try:
        init_db()
    except Exception as e:
        logging.error("Erreur d'initialisation de la base de données : %s", e)
    app = TodoApp()
    app.mainloop()

class TodoApp(ctk.CTk):
    """Application principale : gère le layout et la navigation global."""
    def __init__(self):
        super().__init__()
        self.title("Advanced To-Do List")
        self.geometry("1080x720")
        theme.load_theme()

        self._create_main_container()
        self._create_sidebar()
        # Le bouton du header déclenche le toggle de la sidebar
        self.header.menu_toggle_callback = self.sidebar.toggle
        # La sidebar notifie le header via son callback
        self.sidebar.header_callback = self.header.set_sidebar_expanded
        self.header.set_sidebar_expanded(self.sidebar.expanded)
        # self._initialize_views()  # À activer si besoin

    def _create_main_container(self):
        """
        Crée le conteneur principal, qui occupe toute la fenêtre.
        Le layout interne (Header et content) est géré en grid.
        """
        self.main_container = ctk.CTkFrame(self)
        self.main_container.place(x=0, y=0, relwidth=1, relheight=1)

        self.main_container.grid_rowconfigure(0, weight=0)
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.header = Header(
            self.main_container,
            title=VIEW_TITLES["tasks"],
            menu_toggle_callback=None,  # Assigné ensuite
            share_callback=lambda: logging.info(translations.t("share")),
            login_callback=lambda: logging.info(translations.t("login")),
            user_logged_in=False,
            translations=translations
        )
        self.header.grid(row=0, column=0, sticky="ew")

        self.content_frame = ctk.CTkFrame(self.main_container)
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        # Les autres vues seront placées dans content_frame via .place()

    def _create_sidebar(self):
        """
        Crée et positionne la sidebar en overlay sur la partie gauche de la fenêtre.
        Elle est placée via place() pour éviter d'influencer le layout global.
        """
        sidebar_width = 200
        self.sidebar_container = ctk.CTkFrame(
            self,
            width=sidebar_width,
            corner_radius=0,
            fg_color=theme.get_default_frame_color(),
            bg_color=theme.get_default_frame_color()
        )
        self.sidebar_container.place(x=0, y=0, relheight=1)
        self.sidebar_container.lift()

        self.sidebar = Sidebar(self.sidebar_container, navigate_callback=self._navigate, translations=translations)
        self.sidebar.pack(fill="both", expand=True)

    def _navigate(self, destination):
        """
        Gère la navigation entre vues.
        (À compléter selon votre implémentation des vues.)
        """
        if isinstance(destination, tuple) and destination[0] == "project":
            self.open_project(destination[1])
            self.header.set_title(translations.t("project"))
            return
        try:
            view = self.views[destination]
            self.show_view(view)
            self.header.set_title(translations.t(destination))
        except KeyError:
            logging.warning(f"Destination inconnue : {destination}")

    def show_view(self, view):
        """Place la vue passée en avant (méthode tkraise)."""
        view.tkraise()

    def open_project(self, project_id):
        """Ouvre la vue des tâches avec le projet sélectionné."""
        self.views["tasks"].set_project(project_id)
        self.show_view(self.views["tasks"])

    def _initialize_views(self):
        """
        Initialise et stocke les vues dans un dictionnaire 'views'.
        Appeler cette méthode selon vos besoins.
        """
        # Exemple d'initialisation des vues :
        self.views = {
            "dashboard": DashboardView(self.content_frame),
            "calendar": CalendarView(self.content_frame),
            "tasks": MainView(self.content_frame),
            "projects": ProjectsView(self.content_frame, self.open_project),
            "settings": SettingsView(self.content_frame)
        }
        # Placez chaque vue dans la même cellule pour pouvoir faire du stacking
        for view in self.views.values():
            view.place(relx=0, rely=0, relwidth=1, relheight=1)
        # Affiche la vue principale par défaut
        self.views["tasks"].tkraise()

if __name__ == "__main__":
    run_app()

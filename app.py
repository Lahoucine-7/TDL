"""
app.py

Main entry point for the Advanced To-Do List application.
Initializes the database, sets up the main window, sidebar, header, and various views.
"""

import logging
import customtkinter as ctk
import theme
from database.database import init_db
from views.tasks_view import TasksView
from views.sidebar import Sidebar
from views.header import Header
from views.calendar_view import CalendarView
from views.dashboard_view import DashboardView
from views.settings_view import SettingsView
from views.projects_view import ProjectsView
from utils.translations import TranslationsManager
from controllers.project_controller import ProjectController

# Configure logging for debugging purposes.
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
translations = TranslationsManager(language="fr")

# Mapping of view identifiers to their translated titles.
VIEW_TITLES = {
    "dashboard": translations.t("dashboard"),
    "calendar": translations.t("calendar"),
    "tasks": translations.t("tasks"),
    "projects": translations.t("projects"),
    "settings": translations.t("settings"),
    "project": translations.t("project")
}

def run_app():
    """Initializes the database and runs the application."""
    try:
        init_db()
    except Exception as e:
        logging.error("Database initialization error: %s", e)
    app = TodoApp()
    app.mainloop()

class TodoApp(ctk.CTk):
    """
    Main application window. Contains a sidebar for navigation, a header, and a content frame where
    different views (e.g., Tasks, Calendar, Dashboard) are loaded.
    """
    def __init__(self):
        super().__init__()
        self.title("Advanced To-Do List")
        self.geometry("1080x720")
        theme.load_theme()

        # Set sidebar widths.
        self.sidebar_open_width = 200
        self.sidebar_closed_width = 0

        self._create_sidebar()
        self._create_main_container()

        # Set the menu toggle callback in Header.
        self.header.menu_toggle_callback = self._toggle_sidebar

        self._initialize_views()
        self.bind("<Configure>", self._update_main_container)

    def _create_sidebar(self):
        """Creates and places the sidebar on the left."""
        self.sidebar = Sidebar(
            self,
            width=self.sidebar_open_width,
            navigate_callback=self._navigate,
            translations=translations
        )
        self.sidebar.place(x=0, y=0, relheight=1)

    def _create_main_container(self):
        """Creates the main container which holds the header and content views."""
        self.main_container = ctk.CTkFrame(self)
        self.main_container.place(x=self.sidebar_open_width, y=0)
        self.main_container.grid_rowconfigure(0, weight=0)
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Create and place the header.
        self.header = Header(
            self.main_container,
            title=VIEW_TITLES["tasks"],
            menu_toggle_callback=None,
            share_callback=lambda: logging.info(translations.t("share")),
            login_callback=lambda: logging.info(translations.t("login")),
            user_logged_in=False,
            translations=translations
        )
        self.header.grid(row=0, column=0, sticky="ew")
        
        # Create content frame.
        self.content_frame = ctk.CTkFrame(self.main_container)
        self.content_frame.grid(row=1, column=0, sticky="nsew")

    def _update_geometry(self, sidebar_width):
        """Adjusts the main container size based on sidebar width and window size."""
        total_width = self.winfo_width()
        total_height = self.winfo_height()
        self.main_container.place_configure(
            x=sidebar_width,
            width=total_width - sidebar_width,
            height=total_height
        )

    def _update_main_container(self, event=None):
        """Callback to update the main container geometry when the window is resized."""
        if self.sidebar and self.sidebar.winfo_exists():
            current_sidebar_width = self.sidebar.winfo_width()
            self._update_geometry(current_sidebar_width)

    def _toggle_sidebar(self):
        """
        Toggles the sidebar's visibility by animating its width.
        When collapsed, the sidebar is hidden; when expanded, it is shown.
        """
        current_width = self.sidebar.winfo_width()
        if current_width > (self.sidebar_open_width + self.sidebar_closed_width) / 2:
            self.header.set_sidebar_expanded(False)
            target_width = self.sidebar_closed_width
        else:
            self.header.set_sidebar_expanded(True)
            target_width = self.sidebar_open_width
        self._animate_sidebar_and_content(target_width)

    def _animate_sidebar_and_content(self, target_width, steps=3, delay=20):
        """Animates the sidebar width and updates main container accordingly."""
        current_width = self.sidebar.winfo_width()
        delta = (target_width - current_width) / steps

        def step(i):
            new_width = int(current_width + delta * i)
            self.sidebar.configure(width=new_width)
            self._update_geometry(new_width)
            self.update()
            if i < steps:
                self.after(delay, lambda: step(i + 1))
        step(1)

    def _initialize_views(self):
        """
        Instantiates and places all the views into the content frame.
        Newly created views inherit from BaseView for a unified design.
        """
        self.views = {
            "tasks": TasksView(self.content_frame),
            "calendar": CalendarView(self.content_frame),
            "dashboard": DashboardView(self.content_frame),
            "settings": SettingsView(self.content_frame, change_theme_callback=self._on_change_theme),
            "projects": ProjectsView(self.content_frame, navigate_project_callback=self._navigate)
        }
        for view in self.views.values():
            view.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.views["tasks"].tkraise()

    def _navigate(self, destination):
        """
        Handles navigation between views.
        If the destination is a tuple for a project, it filters TasksView by project.
        Otherwise, it displays the corresponding view.
        """
        if isinstance(destination, tuple) and destination[0] == "project":
            project_id = destination[1]
            self.views["tasks"].set_project(project_id)
            project_ctrl = ProjectController()
            projects = project_ctrl.list_projects()
            project_match = [p for p in projects if p.id == project_id]
            title = project_match[0].name if project_match else VIEW_TITLES["tasks"]
            self.header.set_title(title)
        else:
            try:
                view = self.views[destination]
                view.tkraise()
                self.header.set_title(translations.t(destination))
            except KeyError:
                logging.warning(f"Unknown destination: {destination}")

    def _on_change_theme(self):
        """
        Called when theme or font changes are triggered.
        Reloads the theme and refreshes all views.
        """
        theme.load_theme()
        for v in self.views.values():
            if hasattr(v, "refresh"):
                v.refresh()

if __name__ == "__main__":
    run_app()

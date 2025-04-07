import customtkinter as ctk
from models.database import init_db
from views.main_view import MainView
from views.calendar_view import CalendarView
from views.settings_view import SettingsView

# Initialize the database (create tables if they don't exist)
init_db()

class TodoApp(ctk.CTk):
    """Main application window with sidebar navigation and multiple views."""
    THEMES = ["dark", "light"]

    def __init__(self):
        super().__init__()
        self.title("Advanced To-Do List")
        self.geometry("1080x720")

        # Set initial theme
        self.current_theme = self.THEMES[0]
        ctk.set_appearance_mode(self.current_theme)
        ctk.set_default_color_theme("blue")

        # Create sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")

        # Create main container with grid configuration
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(side="right", expand=True, fill="both")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Initialize views (do not call pack in the view files)
        self.main_view = MainView(self.main_frame)
        self.calendar_view = CalendarView(self.main_frame)
        self.settings_view = SettingsView(self.main_frame, self.toggle_theme)

        # Place views in the same grid cell and show the main view by default
        self.main_view.grid(row=0, column=0, sticky="nsew")
        self.calendar_view.grid(row=0, column=0, sticky="nsew")
        self.settings_view.grid(row=0, column=0, sticky="nsew")
        self.show_view(self.main_view)

        # Create sidebar navigation buttons
        self.add_sidebar_buttons()

    def add_sidebar_buttons(self):
        """Create buttons in the sidebar to navigate between views."""
        btn_tasks = ctk.CTkButton(self.sidebar_frame, text="Tasks", command=lambda: self.show_view(self.main_view))
        btn_calendar = ctk.CTkButton(self.sidebar_frame, text="Calendar", command=lambda: self.show_view(self.calendar_view))
        btn_settings = ctk.CTkButton(self.sidebar_frame, text="Settings", command=lambda: self.show_view(self.settings_view))
        btn_tasks.pack(pady=10, padx=10)
        btn_calendar.pack(pady=10, padx=10)
        btn_settings.pack(pady=10, padx=10)

    def show_view(self, view):
        """Bring the specified view to the front."""
        view.tkraise()

    def toggle_theme(self):
        """Toggle the current theme and update the appearance mode."""
        self.current_theme = self.THEMES[1] if self.current_theme == self.THEMES[0] else self.THEMES[0]
        ctk.set_appearance_mode(self.current_theme)

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()

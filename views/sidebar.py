"""
sidebar.py

Sidebar widget provides navigation between views.
It includes navigation buttons, a search entry, and a collapsible projects section.
"""

import customtkinter as ctk
from controllers.project_controller import ProjectController
from theme import get_font, current_mode, load_icon, get_default_frame_color, get_ctkframe_top_color

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, navigate_callback, translations, width, *args, **kwargs):
        """
        Initializes the Sidebar widget.

        Args:
            master: Parent widget.
            navigate_callback (callable): Function called when a navigation button is clicked.
            translations: Translation manager object.
            width (int): Initial width of the sidebar.
            *args, **kwargs: Additional arguments.
        """
        kwargs["width"] = width
        self.translations = translations
        super().__init__(master, *args, **kwargs)
        self.navigate_callback = navigate_callback
        self.project_controller = ProjectController()
        self.expanded = True
        self.default_width = width
        self.header_callback = None  # Notifies header when toggling

        # Disable geometry propagation to enforce fixed width.
        self.pack_propagate(False)

        dark_mode = (current_mode == "dark")
        self.menu_open_icon = ctk.CTkImage(
            load_icon("icons/menu_open.png", size=(30, 30), invert=dark_mode),
            size=(30, 30)
        )
        self.menu_close_icon = ctk.CTkImage(
            load_icon("icons/menu_close.png", size=(30, 30), invert=dark_mode),
            size=(30, 30)
        )

        self.fixed_height = 600
        self.configure(width=self.default_width, height=self.fixed_height)

        self._build_sidebar()

    def _build_sidebar(self):
        """
        Builds the sidebar by assembling its top, main, and footer sections.
        """
        for widget in self.winfo_children():
            widget.destroy()
        self._create_top_section()
        self._create_main_section()
        self._create_footer_section()

    def _create_top_section(self):
        """
        Creates the top section with a toggle button and search entry.
        """
        self.top_frame = ctk.CTkFrame(
            self,
            fg_color=get_default_frame_color(),
            width=self.default_width,
            height=50
        )
        self.top_frame.place(x=0, y=0)

        self.toggle_button = ctk.CTkButton(
            self.top_frame,
            image=self.menu_open_icon,
            text="",
            command=lambda: self.master._toggle_sidebar(),
            font=get_font("button"),
            width=30,
            height=30,
            fg_color=None
        )
        self.toggle_button.place(x=5, y=5)

        self.search_entry = ctk.CTkEntry(
            self.top_frame,
            placeholder_text=self.translations.t("search_placeholder") if self.translations else "Search",
            font=get_font("text"),
            width=120
        )
        self.search_entry.place(x=60, y=10)

    def _create_main_section(self):
        """
        Creates the main section with navigation buttons and the projects area.
        """
        main_height = self.fixed_height - 100
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color=get_default_frame_color(),
            width=self.default_width,
            height=main_height
        )
        self.main_frame.place(x=0, y=50)

        self.dashboard_btn = ctk.CTkButton(
            self.main_frame,
            text=self.translations.t("dashboard"),
            command=lambda: self.navigate_callback("dashboard"),
            font=get_font("button"),
            width=160
        )
        self.dashboard_btn.place(x=20, y=10)

        self.calendar_btn = ctk.CTkButton(
            self.main_frame,
            text=self.translations.t("calendar"),
            command=lambda: self.navigate_callback("calendar"),
            font=get_font("button"),
            width=160
        )
        self.calendar_btn.place(x=20, y=50)

        self.tasks_btn = ctk.CTkButton(
            self.main_frame,
            text=self.translations.t("tasks"),
            command=lambda: self.navigate_callback("tasks"),
            font=get_font("button"),
            width=160
        )
        self.tasks_btn.place(x=20, y=90)

        self._create_projects_section()

    def _create_projects_section(self):
        """
        Creates the projects section header and populates it with project buttons.
        """
        self.projects_header = ctk.CTkFrame(
            self.main_frame,
            fg_color=get_default_frame_color(),
            width=165,
            height=30
        )
        self.projects_header.place(x=20, y=130)
        self.projects_header.grid_columnconfigure(0, weight=1)
        self.projects_header.grid_columnconfigure(1, weight=0)
        self.projects_header.grid_rowconfigure(0, weight=1)

        self.projects_text_btn = ctk.CTkButton(
            self.projects_header,
            text=self.translations.t("projects"),
            command=lambda: self.navigate_callback("projects"),
            font=get_font("button"),
            fg_color=None,
            corner_radius=8,
            width=120,
            anchor="center"
        )
        self.projects_text_btn.grid(row=0, column=0, sticky="nsew")

        self.projects_toggle_btn = ctk.CTkButton(
            self.projects_header,
            text="▶",
            command=self._toggle_projects,
            font=get_font("button"),
            width=24,
            height=24,
            fg_color=None,
            corner_radius=8
        )
        self.projects_toggle_btn.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        self.projects_frame = ctk.CTkFrame(
            self.main_frame,
            corner_radius=10,
            fg_color=get_ctkframe_top_color(),
            width=160
        )
        self._populate_projects()

    def _populate_projects(self):
        """
        Retrieves projects from the controller and creates buttons for them.
        """
        for widget in self.projects_frame.winfo_children():
            widget.destroy()
        max_chars = 20
        projects = self.project_controller.list_projects() if hasattr(self, "project_controller") else []
        if not projects:
            label = ctk.CTkLabel(
                self.projects_frame,
                text=self.translations.t("no_projects"),
                font=get_font("label"),
                corner_radius=10,
                wraplength=140
            )
            label.place(x=10, y=10)
            label.bind("<Button-1>", lambda e: self.navigate_callback("projects"))
        else:
            y_pos = 10
            for proj in projects:
                display_text = proj.name if len(proj.name) <= max_chars else proj.name[:max_chars] + "..."
                btn = ctk.CTkButton(
                    self.projects_frame,
                    text=display_text,
                    command=lambda p=proj: self.navigate_callback(("project", p.id)),
                    font=get_font("button"),
                    width=140
                )
                # Only x and y are passed to place(), width is set in constructor.
                btn.place(x=10, y=y_pos)
                y_pos += 40

    def _create_footer_section(self):
        """
        Creates the footer section containing a button to open the settings.
        """
        self.footer_frame = ctk.CTkFrame(
            self,
            fg_color=get_default_frame_color(),
            bg_color=get_default_frame_color(),
            width=self.default_width,
            height=50
        )
        self.footer_frame.place(relx=0, rely=1, anchor="sw")
        self.settings_btn = ctk.CTkButton(
            self.footer_frame,
            text=self.translations.t("settings"),
            command=lambda: self.navigate_callback("settings"),
            font=get_font("button"),
            width=160
        )
        self.settings_btn.place(x=20, y=10)

    def _toggle_projects(self):
        """
        Toggles the display of the projects frame.
        """
        if self.projects_frame.winfo_ismapped():
            self.projects_frame.place_forget()
            self.projects_toggle_btn.configure(text="▶")
        else:
            self.projects_frame.place(x=20, y=170)
            self.projects_toggle_btn.configure(text="▼")

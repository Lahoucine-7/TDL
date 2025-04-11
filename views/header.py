"""
header.py

Header widget displayed at the top of the main container.
It is divided into three sections:
  - Left: Menu toggle and search field.
  - Center: View title.
  - Right: Share and User actions.
Includes callbacks for menu, share, and login events.
"""

import customtkinter as ctk
from theme import get_font, load_icon, current_mode

class Header(ctk.CTkFrame):
    def __init__(
        self,
        master,
        title="View Title",
        menu_toggle_callback=None,
        share_callback=None,
        login_callback=None,
        user_logged_in=False,
        user_initials="??",
        translations=None,
        *args,
        **kwargs
    ):
        """
        Initialize Header widget.

        Args:
            master: Parent widget.
            title (str): The display title.
            menu_toggle_callback (callable): Function to toggle the sidebar.
            share_callback (callable): Function called when the share button is pressed.
            login_callback (callable): Function called when the login button is pressed.
            user_logged_in (bool): Whether a user is logged in.
            user_initials (str): Initials to display when a user is logged in.
            translations: Translation manager for i18n.
            *args, **kwargs: Additional arguments.
        """
        self.translations = translations
        super().__init__(master, *args, **kwargs)
        
        # Assign callbacks.
        self.menu_toggle_callback = menu_toggle_callback
        self.share_callback = share_callback
        self.login_callback = login_callback
        self.user_logged_in = user_logged_in
        self.user_initials = user_initials
        self.dropdown_visible = False

        # Load icons based on current mode.
        dark_mode = (current_mode == "dark")
        self.menu_close_icon = ctk.CTkImage(
            load_icon("icons/menu_close.png", size=(30, 30), invert=dark_mode),
            size=(30, 30)
        )
        self.share_icon = ctk.CTkImage(
            load_icon("icons/share.png", size=(30, 30), invert=dark_mode),
            size=(30, 30)
        )
        self.logout_icon = ctk.CTkImage(
            load_icon("icons/logout.png", size=(30, 30), invert=dark_mode),
            size=(30, 30)
        )
        
        # Configure grid layout.
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, minsize=200, weight=0)  # Left
        self.grid_columnconfigure(1, weight=1)              # Center
        self.grid_columnconfigure(2, minsize=70, weight=0)    # Right

        self._create_left_frame()
        self._create_center_frame(title)
        self._create_right_frame()

        # Dropdown frame for user actions.
        self.dropdown_frame = ctk.CTkFrame(self)
        self.set_sidebar_expanded(True)

    def _create_left_frame(self):
        """
        Creates the left section with the menu toggle and search entry.
        """
        self.left_frame = ctk.CTkFrame(self, width=100)
        # Initially hidden when sidebar is expanded.
        self.left_frame.grid(row=0, column=0, sticky="nsw", padx=5, pady=5)
        
        self.menu_button = ctk.CTkButton(
            self.left_frame,
            image=self.menu_close_icon,
            text="",
            command=self.menu_toggle,
            corner_radius=8,
            font=get_font("button"),
            width=30,
            height=30,
            fg_color="transparent"
        )
        self.menu_button.grid(row=0, column=0, sticky="ns", padx=(0, 5))
        
        self.search_entry = ctk.CTkEntry(
            self.left_frame,
            placeholder_text=self.translations.t("search_placeholder") if self.translations else "Search",
            font=get_font("text"),
            width=120
        )
        self.search_entry.grid(row=0, column=1, padx=(0, 5))

    def _create_center_frame(self, title):
        """
        Creates the center section to display the current view title.

        Args:
            title (str): The title text.
        """
        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=get_font("title")
        )
        self.title_label.grid(row=0, column=1, sticky="nsew")

    def _create_right_frame(self):
        """
        Creates the right section with share and login/user button.
        """
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=0, column=2, sticky="nse", padx=5, pady=5)

        self.share_button = ctk.CTkButton(
            self.right_frame,
            image=self.share_icon,
            text="",
            command=self.share,
            corner_radius=8,
            font=get_font("button"),
            width=30,
            height=30,
            fg_color="transparent"
        )
        self.share_button.grid(row=0, column=0, sticky="ns", padx=(0, 5))

        if self.user_logged_in:
            self.user_button = ctk.CTkButton(
                self.right_frame,
                text=self.user_initials,
                width=30,
                height=30,
                command=self.toggle_dropdown,
                corner_radius=8,
                font=get_font("button"),
                fg_color="transparent"
            )
        else:
            self.user_button = ctk.CTkButton(
                self.right_frame,
                text="Login",
                width=30,
                height=40,
                command=self.login,
                corner_radius=8,
                font=get_font("button"),
                fg_color="transparent"
            )
        self.user_button.grid(row=0, column=1, sticky="ns")

    def menu_toggle(self):
        """
        Invokes the menu toggle callback if set.
        """
        if callable(self.menu_toggle_callback):
            self.menu_toggle_callback()

    def share(self):
        """
        Invokes the share callback if set.
        """
        if callable(self.share_callback):
            self.share_callback()

    def login(self):
        """
        Invokes the login callback if set.
        """
        if callable(self.login_callback):
            self.login_callback()

    def toggle_dropdown(self):
        """
        Toggles the display of the user dropdown menu.
        """
        if self.dropdown_visible:
            self.dropdown_frame.grid_forget()
            self.dropdown_visible = False
        else:
            self.dropdown_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5, pady=(0, 5))
            for widget in self.dropdown_frame.winfo_children():
                widget.destroy()
            logout_button = ctk.CTkButton(
                self.dropdown_frame,
                image=self.logout_icon,
                text="",
                command=lambda: print("Logout"),
                corner_radius=8,
                font=get_font("button"),
                width=30,
                height=30,
                fg_color="transparent"
            )
            logout_button.pack(padx=5, pady=5)
            self.dropdown_visible = True

    def set_title(self, title):
        """
        Updates the displayed view title.

        Args:
            title (str): New title text.
        """
        self.title_label.configure(text=title)

    def set_sidebar_expanded(self, expanded: bool):
        """
        Shows or hides the left frame based on sidebar state.

        Args:
            expanded (bool): True if sidebar is expanded, otherwise False.
        """
        if expanded:
            self.left_frame.grid_forget()
            self.menu_button.configure(image=self.menu_close_icon)
        else:
            self.left_frame.grid(row=0, column=0, sticky="nsw", padx=5, pady=5)
            self.menu_button.configure(image=self.menu_close_icon)

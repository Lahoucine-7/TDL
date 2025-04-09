"""
Module Header
Ce widget affiche le header du main_container.
"""

import customtkinter as ctk
from theme import get_font, load_icon, current_mode

class Header(ctk.CTkFrame):
    def __init__(
        self,
        master,
        title="Titre de Vue",
        menu_toggle_callback=None,
        share_callback=None,
        login_callback=None,
        user_logged_in=False,
        user_initials="??",
        translations=None,
        *args,
        **kwargs
    ):
        self.translations = translations
        super().__init__(master, *args, **kwargs)
        # Cette callback sera assignée dans app.py : elle déclenche le toggle de la sidebar.
        self.menu_toggle_callback = menu_toggle_callback
        self.share_callback = share_callback
        self.login_callback = login_callback
        self.user_logged_in = user_logged_in
        self.user_initials = user_initials
        self.dropdown_visible = False

        dark_mode = (current_mode == "dark")
        # Chargement des icônes selon le mode courant
        self.menu_open_icon = ctk.CTkImage(load_icon("icons/menu_open.png", size=(30,30), invert=dark_mode), size=(30,30))
        self.menu_close_icon = ctk.CTkImage(load_icon("icons/menu_close.png", size=(30,30), invert=dark_mode), size=(30,30))
        self.share_icon = ctk.CTkImage(load_icon("icons/share.png", size=(30,30), invert=dark_mode), size=(30,30))
        self.logout_icon = ctk.CTkImage(load_icon("icons/logout.png", size=(30,30), invert=dark_mode), size=(30,30))
        
        # Layout : trois colonnes avec largeur fixe pour left et right
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, minsize=190, weight=0)  # left_frame
        self.grid_columnconfigure(1, weight=1)               # titre (centré)
        self.grid_columnconfigure(2, minsize=70, weight=0)     # right_frame

        # Left frame (contrôle du header : bouton toggle et champ de recherche)
        self.left_frame = ctk.CTkFrame(self, width=100)
        self.left_frame.grid(row=0, column=0, sticky="nsw", padx=5, pady=5)
        self.menu_button = ctk.CTkButton(
            self.left_frame,
            image=self.menu_open_icon,
            text="",
            command=self.menu_toggle,
            corner_radius=8,
            font=get_font("button"),
            width=30,
            height=30,
            fg_color="transparent"
        )
        self.menu_button.grid(row=0, column=0, sticky="ns", padx=(0,5))
        self.search_entry = ctk.CTkEntry(
            self.left_frame,
            placeholder_text=self.translations.t("search_placeholder") if self.translations else "Search",
            font=get_font("text"),
            width=120
        )
        self.search_entry.grid(row=0, column=1, padx=(0,5))

        # Titre centré dans la colonne centrale
        self.title_label = ctk.CTkLabel(self, text=title, font=get_font("title"))
        self.title_label.grid(row=0, column=1, sticky="nsew")

        # Right frame (boutons Share et User)
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
        self.share_button.grid(row=0, column=0, sticky="ns", padx=(0,5))
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
        
        self.dropdown_frame = ctk.CTkFrame(self)

    def menu_toggle(self):
        if callable(self.menu_toggle_callback):
            self.menu_toggle_callback()

    def share(self):
        if callable(self.share_callback):
            self.share_callback()

    def login(self):
        if callable(self.login_callback):
            self.login_callback()

    def toggle_dropdown(self):
        if self.dropdown_visible:
            self.dropdown_frame.grid_forget()
            self.dropdown_visible = False
        else:
            self.dropdown_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5, pady=(0,5))
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
        self.title_label.configure(text=title)

    def set_sidebar_expanded(self, expanded: bool):
        """
        Ajuste la visibilité du left_frame en fonction de l'état de la sidebar.
        - Si expanded est True (sidebar ouverte), on masque le left_frame.
        - Si expanded est False (sidebar fermée), on affiche le left_frame.
        Met à jour aussi l'icône du bouton toggle.
        """
        if expanded:
            # Sidebar ouverte : masquer le contrôle dans le header
            self.left_frame.grid_forget()
            self.menu_button.configure(image=self.menu_open_icon)
        else:
            # Sidebar fermée : afficher le contrôle dans le header
            self.left_frame.grid(row=0, column=0, sticky="nsw", padx=5, pady=5)
            self.menu_button.configure(image=self.menu_close_icon)


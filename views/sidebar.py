"""
Module Sidebar

Ce module définit le widget Sidebar, responsable de la navigation dans l'application.
"""

import customtkinter as ctk
from controllers.project_controller import ProjectController
from theme import get_font, current_mode, load_icon, get_default_frame_color, get_ctkframe_top_color

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, navigate_callback, translations, *args, **kwargs):
        self.translations = translations
        super().__init__(master, *args, **kwargs)
        self.navigate_callback = navigate_callback
        self.project_controller = ProjectController()
        self.expanded = True
        self.default_width = 200  # largeur affichée lorsque la sidebar est déployée
        self.header_callback = None  # pour notifier le header lors du toggle
        dark_mode = (current_mode == "dark")
        self.menu_open_icon = ctk.CTkImage(load_icon("icons/menu_open.png", size=(30,30), invert=dark_mode), size=(30,30))
        self.menu_close_icon = ctk.CTkImage(load_icon("icons/menu_close.png", size=(30,30), invert=dark_mode), size=(30,30))
        self._build_sidebar()

    def _build_sidebar(self):
        # On vide les widgets existants
        for widget in self.winfo_children():
            widget.destroy()
        
        # On fixe la largeur de la sidebar
        self.configure(width=self.default_width)
        
        # Utilisation d'un layout en trois parties : top, main et footer
        self.top_frame = ctk.CTkFrame(self, fg_color=get_default_frame_color())
        self.top_frame.pack(side="top", fill="x", padx=5, pady=5)
        
        # Dans le top_frame, on place le bouton de toggle et le champ de recherche côte à côte.
        self.toggle_button = ctk.CTkButton(
            self.top_frame,
            image=self.menu_open_icon,
            text="",
            command=self.toggle,
            font=get_font("button"),
            width=30,
            height=30,
            fg_color="transparent"
        )
        self.toggle_button.pack(side="left", padx=(0,5))
        
        self.search_entry = ctk.CTkEntry(
            self.top_frame,
            placeholder_text=self.translations.t("search_placeholder") if self.translations else "Search",
            font=get_font("text")
        )
        self.search_entry.pack(side="left", fill="x", expand=True)

        # La partie centrale contient les boutons de navigation
        self.main_frame = ctk.CTkFrame(self, fg_color=get_default_frame_color())
        self.main_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        
        self.dashboard_btn = ctk.CTkButton(
            self.main_frame,
            text=self.translations.t("dashboard"),
            command=lambda: self.navigate_callback("dashboard"),
            font=get_font("button")
        )
        self.dashboard_btn.pack(pady=5, padx=5, fill="x")
        
        self.calendar_btn = ctk.CTkButton(
            self.main_frame,
            text=self.translations.t("calendar"),
            command=lambda: self.navigate_callback("calendar"),
            font=get_font("button")
        )
        self.calendar_btn.pack(pady=5, padx=5, fill="x")
        
        self.tasks_btn = ctk.CTkButton(
            self.main_frame,
            text=self.translations.t("tasks"),
            command=lambda: self.navigate_callback("tasks"),
            font=get_font("button")
        )
        self.tasks_btn.pack(pady=5, padx=5, fill="x")
        
        self.projects_btn = ctk.CTkButton(
            self.main_frame,
            text=self.translations.t("projects"),
            command=self._toggle_projects,
            font=get_font("button")
        )
        self.projects_btn.pack(pady=5, padx=5, fill="x")
        
        self.projects_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color=get_ctkframe_top_color())
        self.projects_frame.pack(pady=5, padx=5, fill="x")
        self._populate_projects()
        
        # Le footer est une zone séparée pour le bouton settings
        self.footer_frame = ctk.CTkFrame(self, fg_color=get_default_frame_color(), bg_color=get_default_frame_color())
        self.footer_frame.pack(side="bottom", fill="x", padx=5, pady=5)
        
        self.settings_btn = ctk.CTkButton(
            self.footer_frame,
            text=self.translations.t("settings"),
            command=lambda: self.navigate_callback("settings"),
            font=get_font("button")
        )
        self.settings_btn.pack(pady=5, padx=5, fill="x")
        
    def toggle(self):
        self.toggle_button.configure(state="disabled")
        if self.expanded:
            self.animate_slide(target_width=0, steps=5, delay=15,
                on_complete=lambda: self.toggle_button.configure(state="normal"))
            self.expanded = False
            self.toggle_button.configure(image=self.menu_close_icon)
        else:
            self.animate_slide(target_width=self.default_width, steps=5, delay=15,
                on_complete=lambda: self.toggle_button.configure(state="normal"))
            self.expanded = True
            self.toggle_button.configure(image=self.menu_open_icon)
            
        if self.header_callback is not None:
            self.header_callback(self.expanded)

        

    
    def animate_slide(self, target_width, steps=10, delay=15, on_complete=None):
        """
        Anime la transition de la largeur vers 'target_width' en 'steps' étapes.
        Le contenu reste visible ou caché progressivement.
        """
        self.pack_propagate(False)
        current_width = self.winfo_width()
        step_size = (target_width - current_width) / steps

        def step(count):
            new_width = int(current_width + step_size * count)
            self.configure(width=new_width)
            self.update_idletasks()
            if count < steps:
                self.after(delay, lambda: step(count + 1))
            else:
                self.configure(width=target_width)
                if on_complete is not None:
                    on_complete()
        step(0)



    def _toggle_projects(self):
        if self.projects_frame.winfo_viewable():
            self.projects_frame.pack_forget()
        else:
            self.projects_frame.pack(pady=5, padx=5, fill="x")

    def _populate_projects(self):
        for widget in self.projects_frame.winfo_children():
            widget.destroy()
        projects = self.project_controller.list_projects()
        if not projects:
            label = ctk.CTkLabel(
                self.projects_frame,
                text="No projects. Click to add.",
                font=get_font("label"),
                corner_radius=10
            )
            label.pack(pady=5)
            label.bind("<Button-1>", lambda e: self.navigate_callback("projects"))
        else:
            for proj in projects:
                btn = ctk.CTkButton(
                    self.projects_frame,
                    text=proj.name,
                    command=lambda p=proj: self.navigate_callback(("project", p.id)),
                    font=get_font("button")
                )
                btn.pack(pady=2, padx=5, fill="x")

# views/projects_view.py

import customtkinter as ctk
import theme
from controllers.project_controller import ProjectController
from models.project import Project
import tkinter.messagebox as messagebox
from controllers.task_controller import TaskController

class ProjectsView(ctk.CTkFrame):
    """
    Vue affichant tous les projets sous forme de cartes.
    
    - Les projets sont affichés en grille (3 par ligne).
    - Chaque carte est un grand carré (400x450 px) avec un fond différent du reste de l'application.
    - On ouvre un projet en cliquant sur la carte.
    - Un bouton rouge "X" permet de supprimer le projet (avec confirmation si le projet a une description ou des tâches).
    - Un bouton "Add Project" et/ou un espace cliquable permet d'ajouter un nouveau projet inline.
    """
    def __init__(self, master, navigate_project_callback, *args, **kwargs):
        """
        :param navigate_project_callback: Fonction appelée avec l'identifiant d'un projet lorsqu'on clique sur une carte.
        """
        super().__init__(master, *args, **kwargs)
        self.controller = ProjectController()
        self.navigate_project_callback = navigate_project_callback
        self._create_widgets()
        self.refresh_projects()

    def _create_widgets(self):
        # Titre de la vue
        self.title_label = ctk.CTkLabel(self, text="Projects", font=theme.get_font(size=22))
        self.title_label.pack(pady=10)

        # Zone pour afficher les projets en grille
        self.projects_container = ctk.CTkScrollableFrame(self)
        self.projects_container.pack(pady=10, padx=10, fill="both", expand=True)
        # Nous utiliserons grid() pour organiser les cartes, sans scrollbar automatique.

        # Bouton "Add Project" dans la vue Projects
        self.add_project_btn = ctk.CTkButton(self, text="+ Add Project", fg_color=theme.COLOR_PRIMARY,
                                              command=self._open_add_project_area)
        self.add_project_btn.pack(pady=10)

    def refresh_projects(self):
        """Rafraîchit la liste des projets dans la zone des cartes."""
        for widget in self.projects_container.winfo_children():
            widget.destroy()
        projects = self.controller.list_projects()
        if not projects:
            no_proj_label = ctk.CTkLabel(self.projects_container,
                                         text="No projects yet. Click here to create one.",
                                         text_color="gray", anchor="center")
            no_proj_label.grid(row=0, column=0, columnspan=3, pady=20)
            no_proj_label.bind("<Button-1>", lambda e: self._open_add_project_area())
        else:
            for idx, project in enumerate(projects):
                row = idx // 3
                col = idx % 3
                card = self._create_project_card(project)
                card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    def _create_project_card(self, project: Project):
        """
        Crée une carte (card) pour un projet.
        La carte a une taille fixe (400x450 px) avec un fond différent.
        Toute la carte est cliquable pour ouvrir le projet, sauf le bouton "X" qui permet de supprimer.
        """
        # Création de la carte avec la taille souhaitée et un fond distinct
        card = ctk.CTkFrame(
            self.projects_container,
            fg_color="#3B3F45",
            corner_radius=10,
            border_width=1,
            border_color=theme.get_border_color(),
            width=400,
            height=450
        )
        card.grid_propagate(False)

        # Fonction pour ouvrir le projet
        def open_project(e=None):
            # Éviter que le clic sur le bouton de suppression déclenche cette fonction
            self.navigate_project_callback(project.id)
        # Appliquer le binding à la carte
        card.bind("<Button-1>", open_project)

        title_label = ctk.CTkLabel(card, text=project.name,
                                    font=theme.get_font(size=24), text_color="white")
        title_label.pack(pady=(20,10), padx=10)
        # On ajoute le binding au titre pour être sûr
        title_label.bind("<Button-1>", open_project)

        # Description (tronquée)
        if project.description:
            short_desc = project.description if len(project.description) < 150 else project.description[:150] + "..."
        else:
            short_desc = "No description"
        desc_label = ctk.CTkLabel(card, text=short_desc,
                                font=theme.get_font(size=18), text_color="gray",
                                wraplength=380, justify="left")
        desc_label.pack(pady=10, padx=10, fill="x")
        # Ajout du binding sur la description
        desc_label.bind("<Button-1>", open_project)

        # Bouton "X" pour supprimer le projet
        delete_btn = ctk.CTkButton(card, text="X", fg_color="#FF6B6B", width=30,
                                command=lambda: self._delete_project(project))
        delete_btn.pack(pady=10)
        # Empêcher la propagation du clic depuis le bouton "X"
        delete_btn.bind("<Button-1>", lambda e: ("break", delete_btn.invoke()))
        return card


    def _delete_project(self, project: Project):
        """
        Demande confirmation pour la suppression du projet.
        Le message propose deux options en une phrase courte :
        "Yes: Delete project and ALL associated tasks; No: Delete project and KEEP tasks; Cancel: Abort"
        """
        # Récupérer les tâches associées au projet
        from controllers.task_controller import TaskController
        task_controller = TaskController()
        tasks = task_controller.list_tasks(project_id=project.id)
        
        if (project.description and project.description.strip()) or (tasks and len(tasks) > 0):
            choice = messagebox.askyesnocancel("Confirm deletion",
                "Delete project and ALL associated tasks?\n"
                "Click Yes to delete project with its tasks.\n"
                "Click No to delete project and KEEP tasks.\n"
                "Click Cancel to abort.")
            if choice is None:  # Annuler
                return
            elif choice is True:
                # Supprimer le projet ET toutes les tâches/sous-tâches
                self.controller.delete_project(project.id, delete_tasks=True)
            else:
                # Supprimer le projet ET dissocier les tâches
                self.controller.delete_project(project.id, delete_tasks=False)
        else:
            # Si le projet est vide, suppression classique
            self.controller.delete_project(project.id, delete_tasks=True)
        self.refresh_projects()

    def _open_add_project_area(self):
        """
        Affiche une zone inline dans la vue Projects pour créer un nouveau projet.
        Un bouton "Create" est utilisé pour valider l'ajout.
        """
        if hasattr(self, "add_area") and self.add_area.winfo_exists():
            return
        row_count = self.projects_container.grid_size()[1]
        self.add_area = ctk.CTkFrame(self.projects_container, fg_color="#555555", corner_radius=10)
        self.add_area.grid(row=row_count, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")
        
        name_entry = ctk.CTkEntry(self.add_area, placeholder_text="Project Name")
        name_entry.pack(pady=5, padx=5, fill="x")
        desc_entry = ctk.CTkTextbox(self.add_area, height=60)  # Ne pas utiliser de placeholder_text (non supporté)
        desc_entry.pack(pady=5, padx=5, fill="x")
        name_entry.focus()

        # Bouton de validation explicite
        create_btn = ctk.CTkButton(self.add_area, text="Create", fg_color=theme.COLOR_PRIMARY,
                                command=lambda: save_project())
        create_btn.pack(pady=5)

        def save_project(e=None):
            name = name_entry.get().strip()
            desc = desc_entry.get("0.0", "end").strip()
            if name:
                self.controller.create_project(name, desc)
            self.add_area.destroy()
            self.refresh_projects()
            
        name_entry.bind("<Return>", save_project)

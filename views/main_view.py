# views/main_view.py

import customtkinter as ctk
from controllers.task_controller import lister_taches, modifier_tache, supprimer_tache, ajouter_tache, ajouter_subtask
from models.task import Task
from views.edit_task_dialog import EditTaskDialog

class MainView(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(fg_color="transparent")
        self.create_widgets()
    
    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Mes Tâches", font=("Helvetica", 20))
        self.label.pack(pady=10)
        
        # Cadre pour la liste des tâches
        self.tasks_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.tasks_frame.pack(pady=5, fill="both", expand=True)
        
        # Bouton + pour ajouter une tâche inline
        self.add_button = ctk.CTkButton(self, text="+", width=40, command=self.open_inline_entry)
        self.add_button.pack(pady=5)
        
        self.refresh_tasks()
    
    def refresh_tasks(self):
        # On vide le cadre et on recharge la liste des tâches
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()
        self.tasks = lister_taches()
        self.tasks.sort(key=lambda t: t.done)
        for task in self.tasks:
            self.add_task_widget(task)
    
    def add_task_widget(self, task):
        # Cadre global pour la ligne de tâche
        line_frame = ctk.CTkFrame(self.tasks_frame, fg_color="transparent", corner_radius=8, height=40)
        line_frame.pack(pady=2, padx=5, fill="x")
        line_frame.pack_propagate(False)

        # Changement du curseur quand on survole le cadre (pour indiquer que c'est cliquable)
        line_frame.bind("<Enter>", lambda e: line_frame.configure(cursor="hand2"))
        line_frame.bind("<Leave>", lambda e: line_frame.configure(cursor=""))

        # Si la tâche possède des détails (date, durée, récurrence), on affiche une flèche pour étendre/cacher
        has_details = task.subtasks or task.description  # Ici, on peut étendre la condition
        # Bouton pour développer/cacher les détails (initialement cachés)
        if has_details:
            self.expanded = False  # État initial
            arrow_text = "►"  # Flèche fermée
            arrow_button = ctk.CTkButton(line_frame, text=arrow_text, width=25, fg_color="transparent", hover_color="#555555",
                                         command=lambda t=task, btn=None: self.toggle_details(t, line_frame, arrow_button))
            arrow_button.pack(side="right", padx=5)
        else:
            # Pour aligner les éléments, on peut ajouter un espace vide
            ctk.CTkLabel(line_frame, text="   ", width=25).pack(side="right", padx=5)
        
        var_done = ctk.BooleanVar(value=task.done)
        checkbox = ctk.CTkCheckBox(line_frame, variable=var_done, text="", width=25,
                                command=lambda t=task, v=var_done: self.on_done_change(t, v.get()))
        checkbox.pack(side="left", padx=5)

        # Label pour le titre et infos résumées
        details = f" • {task.date}" if task.date else ""
        details += f" • {task.duree} min" if task.duree else ""
        label_text = f"{task.titre}{details}"
        if task.done:
            # On peut simuler un texte barré en ajoutant des tildes, ou en modifiant la couleur
            label_text = f"~~{label_text}~~"
        title_label = ctk.CTkLabel(line_frame, text=label_text, anchor="w")
        title_label.pack(side="left", padx=5, fill="x", expand=True)
        title_label.bind("<Button-1>", lambda e, t=task: self.open_edit_popup(t))
        line_frame.bind("<Button-1>", lambda e, t=task: self.open_edit_popup(t))

        # Bouton crayon pour éditer (peut ouvrir la pop-up)
        edit_button = ctk.CTkButton(line_frame, text="✎", width=30, fg_color="blue", hover_color="#555555",
                                    command=lambda t=task: self.open_edit_popup(t))
        edit_button.pack(side="right", padx=5)
        
        # Bouton X rouge pour supprimer la tâche
        delete_button = ctk.CTkButton(line_frame, text="X", width=30, fg_color="red", hover_color="#aa0000",
                                      command=lambda t=task: self.delete_task(t))
        delete_button.pack(side="right", padx=5)
    
    def on_done_change(self, task, done):
        task.done = done

        modifier_tache(task)
        # Puis recharger l'affichage pour réordonner : les tâches validées en bas
        self.refresh_tasks()

    def toggle_details(self, task, parent_frame, arrow_button):
        # Cette fonction peut créer un widget supplémentaire sous la ligne de tâche pour afficher les notes et sous-tâches.
        # Pour l'exemple, on bascule simplement un label d'infos supplémentaires.
        # Vérifier si des détails sont déjà affichés
        details_widget = getattr(parent_frame, "details_widget", None)
        if details_widget:
            # Si le widget existe, le détruire pour le masquer
            details_widget.destroy()
            parent_frame.details_widget = None
            arrow_button.configure(text="►")
        else:
            # Sinon, créer un widget avec les détails (exemple avec les sous-tâches et les notes)
            details_text = ""
            if task.subtasks:
                for sub in task.subtasks:
                    details_text += f" - {sub}\n"
            # On peut ajouter d'autres informations ici (par ex. note, récurrence, etc.)
            details_widget = ctk.CTkLabel(parent_frame, text=details_text, anchor="w", fg_color="#222222")
            details_widget.pack(fill="x", padx=20, pady=2)
            parent_frame.details_widget = details_widget
            arrow_button.configure(text="▼")

    def delete_task(self, task):
        supprimer_tache(task.key)
        self.refresh_tasks()
    
    def open_inline_entry(self):
        # Crée une ligne d'entrée dans tasks_frame pour saisir rapidement le titre
        entry_frame = ctk.CTkFrame(self.tasks_frame, fg_color="#555555", corner_radius=8, height=40)
        entry_frame.pack(pady=2, padx=5, fill="x")
        entry_frame.pack_propagate(False)
        
        entry = ctk.CTkEntry(entry_frame, placeholder_text="Nouveau titre de tâche")
        entry.pack(side="left", padx=5, fill="x", expand=True)
        entry.focus()
        
        var_done = ctk.BooleanVar(value=False)
        checkbox = ctk.CTkCheckBox(entry_frame, variable=var_done, text="", width=25)
        checkbox.pack(side="left", padx=5)
        
        entry.bind("<Return>", lambda e: self.save_new_task(entry.get(), var_done.get(), entry_frame))
        entry.bind("<FocusOut>", lambda e: self.save_new_task(entry.get(), var_done.get(), entry_frame))
    
    def save_new_task(self, titre, done, entry_frame):
        if titre.strip() == "":
            entry_frame.destroy()
            return
        
        new_task = Task(titre=titre)
        new_id = ajouter_tache(new_task)
        if new_id:
            new_task.key = new_id
            self.tasks.append(new_task)
            self.add_task_widget(new_task)
        entry_frame.destroy()
    
    def open_edit_popup(self, task):
        # Ouvre une pop-up d'édition centrée sur la fenêtre principale et modal
        EditTaskDialog(self.master, task, self.refresh_tasks)

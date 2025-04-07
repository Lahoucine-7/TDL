# views/main_view.py

import customtkinter as ctk
import theme
from controllers.task_controller import TaskController

class MainView(ctk.CTkFrame):
    """
    Vue principale : affiche la liste des tâches, avec un bouton d'ajout.
    Ne fait que de l'affichage : toute la logique est dans TaskController.
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(fg_color="transparent")

        # Instancie le contrôleur
        self.controller = TaskController()

        self.normal_font = theme.get_font()
        self.overstrike_font = theme.get_font(overstrike=True)
        self.task_entry_active = False

        self._create_widgets()
        self.refresh_tasks()

    def _create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="My Tasks", font=self.normal_font)
        self.title_label.pack(pady=10)

        self.tasks_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.tasks_frame.pack(pady=5, fill="both", expand=True)

        self.add_button = ctk.CTkButton(self, text="+", width=40, command=self._open_inline_entry)
        self.add_button.pack(pady=5)

    def refresh_tasks(self):
        """Rafraîchit l'affichage des tâches en les récupérant via le contrôleur."""
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        tasks = self.controller.list_tasks()
        if not tasks:
            self._create_empty_label()
        else:
            # Tri : non faites puis faites
            tasks.sort(key=lambda t: (t.done, t.key if t.key else 0))
            for task in tasks:
                self._add_task_widget(task)

    def _create_empty_label(self):
        """
        Affiche un label "No tasks" cliquable pour créer une tâche inline.
        """
        label = ctk.CTkLabel(
            self.tasks_frame,
            text="No tasks yet. Click here to add a task",
            text_color="gray",
            anchor="center"
        )
        label.pack(pady=10, fill="x")

        # On bind un clic pour déclencher la création inline
        label.bind("<Button-1>", lambda e: self._on_empty_label_clicked(label))

    def _on_empty_label_clicked(self, label_widget):
        """
        Détruit le label "No tasks yet" et le remplace par un champ inline
        permettant de créer une nouvelle tâche.
        """
        label_widget.destroy()
        entry = ctk.CTkEntry(self.tasks_frame, placeholder_text="New task title")
        entry.pack(pady=10, fill="x", padx=5)
        entry.focus()

        def _save(_event=None):
            title = entry.get().strip()
            entry.destroy()
            if title:
                # Appel du contrôleur pour créer la tâche
                self.controller.create_task(title=title)
            self.refresh_tasks()

        entry.bind("<Return>", _save)
        entry.bind("<FocusOut>", _save)


    def _open_inline_entry(self):
        """Affiche un champ inline pour ajouter une nouvelle tâche."""
        if self.task_entry_active:
            return
        self.task_entry_active = True

        entry_frame = ctk.CTkFrame(self.tasks_frame, fg_color="#555555", corner_radius=8)
        entry_frame.pack(pady=2, padx=5, fill="x")

        entry = ctk.CTkEntry(entry_frame, placeholder_text="New task title")
        entry.pack(side="left", padx=5, fill="x", expand=True)
        entry.focus()

        def _save_entry(_event=None):
            title = entry.get().strip()
            self.task_entry_active = False
            entry_frame.destroy()
            if title:
                self.controller.create_task(title=title)
            self.refresh_tasks()

        entry.bind("<Return>", _save_entry)
        entry.bind("<FocusOut>", _save_entry)

    def _add_task_widget(self, task):
        row_frame = ctk.CTkFrame(self.tasks_frame, fg_color="transparent", corner_radius=8)
        row_frame.pack(pady=2, padx=5, fill="x")

        done_var = ctk.BooleanVar(value=task.done)
        checkbox = ctk.CTkCheckBox(
            row_frame, variable=done_var, text="", width=25,
            command=lambda: self._on_done_change(task, done_var.get())
        )
        checkbox.pack(side="left", padx=5)

        details_str = ""
        if task.date:
            details_str += f" • {task.date}"
        if task.duration:
            details_str += f" • {task.duration} min"

        label_text = f"{task.title}{details_str}"
        font_to_use = self.overstrike_font if task.done else self.normal_font
        text_color = "gray" if task.done else None

        title_label = ctk.CTkLabel(row_frame, text=label_text,
                                   anchor="w", font=font_to_use, text_color=text_color)
        title_label.pack(side="left", padx=5, fill="x", expand=True)

        # Bouton "Delete"
        delete_btn = ctk.CTkButton(row_frame, text="X", width=30, fg_color="red",
                                   command=lambda: self._on_delete_task(task.key))
        delete_btn.pack(side="right", padx=5)

        # Bouton "Edit" (ouvrira un EditTaskDialog)
        edit_btn = ctk.CTkButton(row_frame, text="✎", width=30, fg_color="blue",
                                 command=lambda: self._on_edit_task(task))
        edit_btn.pack(side="right", padx=5)

    def _on_done_change(self, task, is_done):
        """Marque la tâche comme (non) terminée via le contrôleur."""
        self.controller.mark_task_done(task.key, is_done)
        self.refresh_tasks()

    def _on_delete_task(self, task_key):
        self.controller.delete_task(task_key)
        self.refresh_tasks()

    def _on_edit_task(self, task):
        """
        Ouvre la fenêtre d'édition, en lui passant la callback refresh_tasks.
        """
        from views.edit_task_dialog import EditTaskDialog
        EditTaskDialog(self.master, task, self.refresh_tasks, self.controller)

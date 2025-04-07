# views/edit_task_dialog.py

import customtkinter as ctk
from controllers.task_controller import modifier_tache

class EditTaskDialog(ctk.CTkToplevel):
    def __init__(self, master, task, refresh_callback, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.task = task
        self.refresh_callback = refresh_callback
        self.title("Modifier la tâche")
        self.geometry("400x400")

        # Rendre la fenêtre modale
        self.transient(master)
        self.grab_set()
        
        # Assurer qu'elle se positionne au-dessus et qu'elle est centrée
        self.center_window()
        self.lift()
        self.attributes("-topmost", True)
        # Après quelques millisecondes, on désactive l'attribut topmost pour ne pas gêner
        self.after(10, lambda: self.attributes("-topmost", False))

        self.create_widgets()

    def center_window(self):
        # On met à jour les "idletasks" pour obtenir des dimensions précises
        self.update_idletasks()
        popup_width = self.winfo_width()
        popup_height = self.winfo_height()
        
        # Récupérer les dimensions et la position de la fenêtre principale
        master = self.master
        master.update_idletasks()
        master_x = master.winfo_rootx()
        master_y = master.winfo_rooty()
        master_width = master.winfo_width()
        master_height = master.winfo_height()
        
        # Calculer la position pour centrer la pop-up par rapport à la fenêtre principale
        pos_x = master_x + (master_width - popup_width) // 2
        pos_y = master_y + (master_height - popup_height) // 2
        
        self.geometry(f"+{pos_x}+{pos_y}")

    def create_widgets(self):
        # Afficher le titre de la tâche dans un champ modifiable
        self.label_title = ctk.CTkLabel(self, text="Titre")
        self.label_title.pack(pady=5)
        self.entry_title = ctk.CTkEntry(self)
        self.entry_title.insert(0, self.task.titre)
        self.entry_title.pack(pady=5)

        # Exemple pour la date
        self.label_date = ctk.CTkLabel(self, text="Date (YYYY-MM-DD)")
        self.label_date.pack(pady=5)
        self.entry_date = ctk.CTkEntry(self)
        self.entry_date.insert(0, self.task.date if self.task.date else "")
        self.entry_date.pack(pady=5)

        # Ajoute d'autres champs (heure, durée, description, etc.) si nécessaire
        # Ici, on peut enregistrer automatiquement dès que l'utilisateur quitte le champ
        self.entry_title.bind("<FocusOut>", self.save_changes)
        self.entry_date.bind("<FocusOut>", self.save_changes)

    def save_changes(self, event=None):
        # Mettre à jour l'objet task
        self.task.titre = self.entry_title.get()
        self.task.date = self.entry_date.get()
        # Ici, tu peux mettre à jour d'autres champs
        # Enregistrer automatiquement sans bouton de validation
        modifier_tache(self.task)
        self.refresh_callback()

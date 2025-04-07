# views/settings_view.py

import customtkinter as ctk
import tkinter.filedialog as filedialog
import csv, json
from controllers.task_controller import lister_taches

class SettingsView(ctk.CTkFrame):
    def __init__(self, master, change_theme_callback, *args, **kwargs):
        """
        :param master: Parent widget.
        :param change_theme_callback: Fonction callback pour changer le thème dans l'application.
        """
        super().__init__(master, *args, **kwargs)
        self.change_theme_callback = change_theme_callback
        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Paramètres", font=("Helvetica", 20))
        self.label.pack(pady=10)
        
        # Bouton pour changer le thème
        self.theme_button = ctk.CTkButton(self, text="Changer thème", command=self.change_theme)
        self.theme_button.pack(pady=10)
        
        # Bouton pour exporter en CSV
        self.export_csv_button = ctk.CTkButton(self, text="Exporter en CSV", command=self.export_csv)
        self.export_csv_button.pack(pady=10)
        
        # Bouton pour exporter en JSON
        self.export_json_button = ctk.CTkButton(self, text="Exporter en JSON", command=self.export_json)
        self.export_json_button.pack(pady=10)

    def change_theme(self):
        # Appelle le callback fourni pour changer le thème
        self.change_theme_callback()

    def export_csv(self):
        tasks = lister_taches()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["key", "titre", "description", "date", "heure", "duree"])
                for task in tasks:
                    writer.writerow([task.key, task.titre, task.description, task.date, task.heure, task.duree])
            print("Export CSV terminé")

    def export_json(self):
        tasks = lister_taches()
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            tasks_data = [task.to_dict() for task in tasks]
            with open(file_path, "w", encoding="utf-8") as jsonfile:
                json.dump(tasks_data, jsonfile, ensure_ascii=False, indent=4)
            print("Export JSON terminé")

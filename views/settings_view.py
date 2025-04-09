# views/settings_view.py

import customtkinter as ctk
import tkinter.filedialog as filedialog
import csv
import json
import theme
from controllers.task_controller import TaskController

class SettingsView(ctk.CTkFrame):
    """
    Vue de réglages : changement de thème, export CSV/JSON, choix de police.
    """
    def __init__(self, master, change_theme_callback, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.controller = TaskController()
        self.change_theme_callback = change_theme_callback
        self._create_widgets()

    def _create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="Settings", font=theme.get_font())
        self.title_label.pack(pady=10)
        self.theme_button = ctk.CTkButton(self, text="Toggle Theme", command=self._on_toggle_theme)
        self.theme_button.pack(pady=10)
        self.font_label = ctk.CTkLabel(self, text="Select Font", font=theme.get_font())
        self.font_label.pack(pady=(10,0))
        self.font_combobox = ctk.CTkComboBox(self, values=theme.AVAILABLE_FONTS)
        self.font_combobox.set(theme.DEFAULT_FONT_FAMILY)
        self.font_combobox.pack(pady=10)
        self.font_combobox.bind("<<ComboboxSelected>>", self._on_font_change)
        export_csv_btn = ctk.CTkButton(self, text="Export CSV", command=self._export_csv)
        export_csv_btn.pack(pady=10)
        export_json_btn = ctk.CTkButton(self, text="Export JSON", command=self._export_json)
        export_json_btn.pack(pady=10)

    def _on_toggle_theme(self):
        self.change_theme_callback()

    def _on_font_change(self, event):
        selected_font = self.font_combobox.get()
        theme.DEFAULT_FONT_FAMILY = selected_font
        self.change_theme_callback()

    def _export_csv(self):
        tasks = self.controller.list_tasks()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                with open(file_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["id", "title", "description", "date", "time", "duration", "done", "project_id"])
                    for t in tasks:
                        writer.writerow([t.id, t.title, t.description, t.date, t.time, t.duration, t.done, t.project_id])
                print("CSV export successful.")
            except Exception as e:
                print(f"Error exporting CSV: {e}")

    def _export_json(self):
        tasks = self.controller.list_tasks()
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                data = [t.__dict__ for t in tasks]
                with open(file_path, "w", encoding="utf-8") as jf:
                    json.dump(data, jf, ensure_ascii=False, indent=4)
                print("JSON export successful.")
            except Exception as e:
                print(f"Error exporting JSON: {e}")

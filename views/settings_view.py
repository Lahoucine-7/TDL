"""
settings_view.py

SettingsView allows users to toggle the theme, change the font, and export tasks as CSV or JSON.
It inherits from BaseView for unified theme and translation management.
"""

import customtkinter as ctk
import tkinter.filedialog as filedialog
import csv
import json
import theme
from controllers.task_controller import TaskController
from views.base_view import BaseView

class SettingsView(BaseView):
    def __init__(self, master, change_theme_callback, *args, **kwargs):
        """
        Initializes SettingsView.

        Args:
            master: Parent widget.
            change_theme_callback (callable): Function to be called when a theme/font change occurs.
            *args, **kwargs: Additional arguments.
        """
        super().__init__(master, *args, **kwargs)
        self.controller = TaskController()
        self.change_theme_callback = change_theme_callback
        self._create_widgets()

    def _create_widgets(self):
        """
        Creates and places widgets for changing the theme, selecting fonts, and exporting data.
        """
        self.title_label = ctk.CTkLabel(
            self,
            text=self.translations.t("settings"),
            font=theme.get_font("title")
        )
        self.title_label.pack(pady=10)
        
        # Button to toggle theme.
        self.theme_button = ctk.CTkButton(
            self,
            text=self.translations.t("toggle_theme") if hasattr(self.translations, "t") else "Toggle Theme",
            command=self._on_toggle_theme
        )
        self.theme_button.pack(pady=10)
        
        # Font selection.
        self.font_label = ctk.CTkLabel(
            self,
            text=self.translations.t("select_font") if hasattr(self.translations, "t") else "Select Font",
            font=theme.get_font("text")
        )
        self.font_label.pack(pady=(10, 0))
        
        self.font_combobox = ctk.CTkComboBox(
            self,
            values=getattr(theme, "AVAILABLE_FONTS", ["Roboto", "Helvetica", "Inter"])
        )
        self.font_combobox.set(getattr(theme, "DEFAULT_FONT_FAMILY", "Roboto"))
        self.font_combobox.pack(pady=10)
        self.font_combobox.bind("<<ComboboxSelected>>", self._on_font_change)
        
        # Export buttons.
        export_csv_btn = ctk.CTkButton(
            self,
            text="Export CSV",
            command=self._export_csv
        )
        export_csv_btn.pack(pady=10)
        
        export_json_btn = ctk.CTkButton(
            self,
            text="Export JSON",
            command=self._export_json
        )
        export_json_btn.pack(pady=10)

    def _on_toggle_theme(self):
        """
        Called when the toggle theme button is pressed.
        Invokes the external theme change callback.
        """
        self.change_theme_callback()

    def _on_font_change(self, event):
        """
        Called when the font selection changes.
        Updates the default font in theme and triggers a theme reload.
        """
        selected_font = self.font_combobox.get()
        setattr(theme, "DEFAULT_FONT_FAMILY", selected_font)
        self.change_theme_callback()

    def _export_csv(self):
        """
        Exports tasks to a CSV file.
        """
        tasks = self.controller.list_tasks()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                with open(file_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["id", "title", "description", "due_date", "time", "duration", "done", "project_id"])
                    for t in tasks:
                        writer.writerow([t.id, t.title, t.description, t.due_date, t.time, t.duration, t.done, t.project_id])
                print("CSV export successful.")
            except Exception as e:
                print(f"Error exporting CSV: {e}")

    def _export_json(self):
        """
        Exports tasks to a JSON file.
        """
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

    def refresh(self) -> None:
        """
        Refresh method for SettingsView.
        May be used to update settings or refresh exportable data.
        """
        pass

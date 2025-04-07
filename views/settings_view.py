import customtkinter as ctk
import tkinter.filedialog as filedialog
import csv, json
from controllers.task_controller import list_tasks
import theme

class SettingsView(ctk.CTkFrame):
    """View for application settings (theme, export, and font selection)."""
    def __init__(self, master, change_theme_callback, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.change_theme_callback = change_theme_callback
        self.create_widgets()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="Settings", font=theme.get_font())
        self.title_label.pack(pady=10)

        # Button to change theme
        self.theme_button = ctk.CTkButton(self, text="Change Theme", command=self.change_theme)
        self.theme_button.pack(pady=10)

        # Font selection
        self.font_label = ctk.CTkLabel(self, text="Select Font", font=theme.get_font())
        self.font_label.pack(pady=(10,0))
        self.font_combobox = ctk.CTkComboBox(self, values=theme.AVAILABLE_FONTS)
        self.font_combobox.set(theme.DEFAULT_FONT_FAMILY)
        self.font_combobox.pack(pady=10)
        self.font_combobox.bind("<<ComboboxSelected>>", self.on_font_change)

        # Export options
        self.export_csv_button = ctk.CTkButton(self, text="Export CSV", command=self.export_csv)
        self.export_csv_button.pack(pady=10)
        self.export_json_button = ctk.CTkButton(self, text="Export JSON", command=self.export_json)
        self.export_json_button.pack(pady=10)

    def on_font_change(self, event):
        """Update the global font setting and refresh the UI if necessary."""
        selected_font = self.font_combobox.get()
        theme.DEFAULT_FONT_FAMILY = selected_font  # update the default font in the theme module
        # Optionally, refresh the entire UI here
        self.change_theme_callback()

    def change_theme(self):
        self.change_theme_callback()

    def export_csv(self):
        tasks = list_tasks()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                import csv
                writer = csv.writer(csvfile)
                writer.writerow(["key", "title", "description", "date", "time", "duration", "done"])
                for task in tasks:
                    writer.writerow([task.key, task.title, task.description, task.date, task.time, task.duration, task.done])
            print("CSV export completed.")

    def export_json(self):
        tasks = list_tasks()
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            import json
            tasks_data = [task.to_dict() for task in tasks]
            with open(file_path, "w", encoding="utf-8") as jsonfile:
                json.dump(tasks_data, jsonfile, ensure_ascii=False, indent=4)
            print("JSON export completed.")

# views/edit_task_dialog.py

import customtkinter as ctk
from tkcalendar import DateEntry
import theme

class EditTaskDialog(ctk.CTkToplevel):
    """
    Permet d'éditer une tâche et ses sous-tâches,
    appelle le TaskController pour toute modification.
    """
    def __init__(self, master, task, refresh_callback, task_controller, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.task = task
        self.refresh_callback = refresh_callback
        self.controller = task_controller

        self.title("Edit Task")
        self.geometry("400x600")

        self.transient(master)
        self.grab_set()
        self.lift()

        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=380, height=500)
        self.scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.content_frame = self.scrollable_frame

        self.footer_frame = ctk.CTkFrame(self, height=50, fg_color="transparent")
        self.footer_frame.pack(fill="x", padx=10, pady=10)

        self.normal_font = theme.get_font()
        self.overstrike_font = theme.get_font(overstrike=True)

        self._create_widgets()
        self._load_subtasks()

    def _create_widgets(self):
        # Task form
        label_title = ctk.CTkLabel(self.content_frame, text="Title")
        label_title.pack(pady=(15,5))
        self.entry_title = ctk.CTkEntry(self.content_frame, width=300)
        self.entry_title.insert(0, self.task.title)
        self.entry_title.pack(pady=5)

        label_desc = ctk.CTkLabel(self.content_frame, text="Description")
        label_desc.pack(pady=(15,5))
        self.text_desc = ctk.CTkTextbox(self.content_frame, width=300, height=90)
        if self.task.description:
            self.text_desc.insert("0.0", self.task.description)
        self.text_desc.pack(pady=5)

        dt_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        dt_frame.pack(pady=(15,5), fill="x", padx=5)
        dt_frame.grid_columnconfigure(0, weight=1)
        dt_frame.grid_columnconfigure(1, weight=1)
        dt_frame.grid_columnconfigure(2, weight=1)

        ctk.CTkLabel(dt_frame, text="Date").grid(row=0, column=0, padx=2)
        self.date_entry = DateEntry(dt_frame, date_pattern="yyyy-mm-dd", width=10)
        if self.task.date:
            self.date_entry.set_date(self.task.date)
        self.date_entry.grid(row=1, column=0, padx=2)

        ctk.CTkLabel(dt_frame, text="Time").grid(row=0, column=1, padx=2)
        time_options = [f"{h:02d}:{m:02d}" for h in range(24) for m in (0,15,30,45)]
        self.time_combobox = ctk.CTkComboBox(dt_frame, values=time_options, width=70)
        self.time_combobox.set(self.task.time if self.task.time in time_options else time_options[0])
        self.time_combobox.grid(row=1, column=1, padx=2)

        ctk.CTkLabel(dt_frame, text="Duration").grid(row=0, column=2, padx=2)
        duration_options = [str(x) for x in (5,10,15,20,30,45,60,90,120,240,480)]
        self.duration_combobox = ctk.CTkComboBox(dt_frame, values=duration_options, width=70)
        self.duration_combobox.set(str(self.task.duration) if str(self.task.duration) in duration_options else duration_options[0])
        self.duration_combobox.grid(row=1, column=2, padx=2)

        # Subtasks
        subtasks_header = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        subtasks_header.pack(pady=(15,5), fill="x", padx=5)
        subtasks_header.grid_columnconfigure(0, weight=1)
        subtasks_header.grid_columnconfigure(1, weight=2)
        subtasks_header.grid_columnconfigure(2, weight=1)

        ctk.CTkLabel(subtasks_header, text="Subtasks", font=self.normal_font).grid(row=0, column=1, sticky="nsew")
        add_btn = ctk.CTkButton(
            subtasks_header, text="+", width=30, fg_color="blue",
            command=self._open_add_subtask_entry
        )
        add_btn.grid(row=0, column=2, sticky="e", padx=5)

        self.subtasks_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.subtasks_container.pack(pady=5, fill="both", expand=False)

        # Validate button
        validate_btn = ctk.CTkButton(self.footer_frame, text="Validate", command=self._save_changes)
        validate_btn.pack(side="right", padx=5)

    def _load_subtasks(self):
        # Récupère la liste de subtasks via le contrôleur
        self.task.subtasks = self.controller.list_subtasks(self.task.key)
        self._update_subtasks_list()

    def _update_subtasks_list(self):
        for widget in self.subtasks_container.winfo_children():
            widget.destroy()

        if not self.task.subtasks:
            example_label = ctk.CTkLabel(
                self.subtasks_container, text="Click here to add a subtask",
                text_color="gray", anchor="center"
            )
            example_label.pack(pady=10, fill="x")
            example_label.bind("<Button-1>", lambda e: self._edit_example_subtask(example_label))
        else:
            self.task.subtasks.sort(key=lambda s: (s.done, s.key if s.key else 0))
            for sub in self.task.subtasks:
                self._add_subtask_widget(sub)

    def _add_subtask_widget(self, sub):
        sub_frame = ctk.CTkFrame(self.subtasks_container, fg_color="transparent")
        sub_frame.pack(fill="x", padx=5, pady=2)

        done_var = ctk.BooleanVar(value=sub.done)
        checkbox = ctk.CTkCheckBox(
            sub_frame, variable=done_var, text="", width=20,
            command=lambda s=sub, v=done_var: self._on_subtask_done_change(s, v.get())
        )
        checkbox.pack(side="left", padx=5)

        font_to_use = self.overstrike_font if sub.done else self.normal_font
        text_color = "gray" if sub.done else None
        sub_label = ctk.CTkLabel(sub_frame, text=sub.title, anchor="w",
                                 font=font_to_use, text_color=text_color)
        sub_label.pack(side="left", fill="x", expand=True)
        sub_label.bind("<Button-1>", lambda e, s=sub, f=sub_frame: self._edit_subtask_inline(s, f))

        del_btn = ctk.CTkButton(
            sub_frame, text="X", width=25, fg_color="red",
            command=lambda s=sub: self._on_delete_subtask(s)
        )
        del_btn.pack(side="right", padx=5)

    def _on_subtask_done_change(self, subtask, done_val):
        subtask.done = done_val
        self.controller.update_subtask(subtask)
        self._load_subtasks()

    def _edit_example_subtask(self, example_label):
        example_label.destroy()
        entry = ctk.CTkEntry(self.subtasks_container, placeholder_text="New subtask title")
        entry.pack(fill="x", padx=5, pady=5)
        entry.focus()

        def _save_inline(_event=None):
            title = entry.get().strip()
            entry.destroy()
            if title:
                self.controller.create_subtask(self.task.key, title=title)
            self._load_subtasks()

        entry.bind("<Return>", _save_inline)
        entry.bind("<FocusOut>", _save_inline)

    def _open_add_subtask_entry(self):
        entry_frame = ctk.CTkFrame(self.subtasks_container, fg_color="#555555", corner_radius=8)
        entry_frame.pack(pady=2, padx=5, fill="x")

        entry = ctk.CTkEntry(entry_frame, placeholder_text="New subtask title")
        entry.pack(side="left", padx=5, fill="x", expand=True)
        entry.focus()

        def _save_entry(_event=None):
            title = entry.get().strip()
            if title:
                self.controller.create_subtask(self.task.key, title=title)
            entry_frame.destroy()
            self._load_subtasks()

        entry.bind("<Return>", _save_entry)
        entry.bind("<FocusOut>", _save_entry)

    def _edit_subtask_inline(self, subtask, container_frame):
        for widget in container_frame.winfo_children():
            widget.destroy()

        edit_entry = ctk.CTkEntry(container_frame, width=200)
        edit_entry.insert(0, subtask.title)
        edit_entry.pack(side="left", padx=5, fill="x", expand=True)
        edit_entry.focus()

        def _save_edit(_event=None):
            new_title = edit_entry.get().strip()
            if new_title:
                subtask.title = new_title
                self.controller.update_subtask(subtask)
            self._load_subtasks()

        edit_entry.bind("<Return>", _save_edit)
        edit_entry.bind("<FocusOut>", _save_edit)

    def _on_delete_subtask(self, subtask):
        self.controller.delete_subtask(subtask.key)
        self._load_subtasks()

    def _save_changes(self):
        # Mettre à jour la tâche (title, desc, date, time, duration)
        self.task.title = self.entry_title.get().strip()
        self.task.description = self.text_desc.get("0.0", "end").strip()
        self.task.date = self.date_entry.get_date().strftime("%Y-%m-%d")
        self.task.time = self.time_combobox.get()
        try:
            self.task.duration = int(self.duration_combobox.get())
        except ValueError:
            self.task.duration = None

        self.controller.update_task(self.task)
        self.refresh_callback()
        self.destroy()

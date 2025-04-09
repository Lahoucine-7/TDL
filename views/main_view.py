# views/main_view.py

import customtkinter as ctk
from tkcalendar import DateEntry
import theme
from controllers.task_controller import TaskController
from models.task import Task

class MainView(ctk.CTkFrame):
    """
    Vue principale affichant la liste des tâches.
    Les tâches peuvent être filtrées par projet via MainView.set_project(project_id).
    Utilise un dictionnaire (self.task_widgets) pour mettre à jour uniquement les widgets modifiés.
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(fg_color="transparent")
        
        self.controller = TaskController()
        self.normal_font = theme.get_font()
        self.overstrike_font = theme.get_font(overstrike=True)
        self.task_entry_active = False
        self.current_project = None  # Pour filtrer par projet

        self.task_widgets = {}
        self._create_widgets()
        self.refresh_tasks()

    def set_project(self, project_id):
        """Filtre les tâches par project_id (None pour toutes)."""
        self.current_project = project_id
        self.refresh_tasks()

    def _create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="My Tasks", font=self.normal_font)
        self.title_label.pack(pady=10)
        self.tasks_frame = ctk.CTkFrame(self, corner_radius=8, border_width=2, border_color=theme.get_border_color())
        self.tasks_frame.pack(pady=10, fill="both", expand=True)
        self.add_button = ctk.CTkButton(self, text="+", width=40, fg_color=theme.COLOR_PRIMARY, command=self._open_inline_entry)
        self.add_button.pack(pady=10)

    def refresh_tasks(self):
        for widget in self.task_widgets.values():
            widget.destroy()
        self.task_widgets = {}

        if hasattr(self, "current_project") and self.current_project is not None:
            tasks = self.controller.list_tasks(project_id=self.current_project)
        else:
            tasks = self.controller.list_tasks()

        if not tasks:
            self._create_empty_label()
            return

        for task in tasks:
            widget = self._create_task_widget(task)
            self.task_widgets[task.id] = widget

    def _create_empty_label(self):
        label = ctk.CTkLabel(self.tasks_frame, text="No tasks yet. Click here to add a task", text_color="gray", anchor="center")
        label.pack(pady=10, fill="x")
        label.bind("<Button-1>", lambda e: self._on_empty_label_clicked(label))

    def _on_empty_label_clicked(self, label_widget):
        label_widget.destroy()
        entry = ctk.CTkEntry(self.tasks_frame, placeholder_text="New task title")
        entry.pack(pady=10, fill="x", padx=5)
        entry.focus()
        def _save(e=None):
            title = entry.get().strip()
            entry.destroy()
            if title:
                self.controller.create_task(title=title, project_id=self.current_project)
            self.refresh_tasks()
        entry.bind("<Return>", _save)
        entry.bind("<FocusOut>", _save)

    def _open_inline_entry(self):
        if self.task_entry_active:
            return
        self.task_entry_active = True
        entry_frame = ctk.CTkFrame(self.tasks_frame, fg_color="#555555", corner_radius=8)
        entry_frame.pack(pady=2, padx=5, fill="x")
        entry = ctk.CTkEntry(entry_frame, placeholder_text="New task title")
        entry.pack(side="left", padx=5, fill="x", expand=True)
        entry.focus()
        def _save_entry(e=None):
            title = entry.get().strip()
            self.task_entry_active = False
            entry_frame.destroy()
            if title:
                self.controller.create_task(title=title, project_id=self.current_project)
            self.refresh_tasks()
        entry.bind("<Return>", _save_entry)
        entry.bind("<FocusOut>", _save_entry)

    def _create_task_widget(self, task):
        container = ctk.CTkFrame(self.tasks_frame, fg_color=theme.COLOR_TASK_BG, corner_radius=10, border_width=1, border_color=theme.get_border_color())
        container.pack(pady=2, padx=5, fill="x")
        container.task = task

        header_frame = ctk.CTkFrame(container, fg_color="transparent", corner_radius=10)
        header_frame.pack(fill="x")

        done_var = ctk.BooleanVar(value=task.done)
        checkbox = ctk.CTkCheckBox(header_frame, variable=done_var, text="", width=25,
                                    command=lambda e=None: self._on_done_change(task.id, done_var.get()))
        checkbox.pack(side="left", padx=5)

        title_label = ctk.CTkLabel(header_frame, text=task.title, anchor="w",
                                    font=self.overstrike_font if task.done else self.normal_font,
                                    text_color="gray" if task.done else "white")
        title_label.pack(side="left", padx=5, fill="x", expand=True)
        title_label.bind("<Button-1>", lambda e: self._edit_task_inline(task, title_label, header_frame))
        container.title_label = title_label

        delete_btn = ctk.CTkButton(header_frame, text="X", width=30, fg_color=theme.COLOR_DELETE,
                                    command=lambda e=None: self._on_delete_task(task.id))
        delete_btn.pack(side="right", padx=5)

        arrow_btn = ctk.CTkButton(header_frame, text="►", width=30, fg_color="transparent",
                                   command=lambda e=None: self._toggle_details(container))
        arrow_btn.pack(side="right", padx=5)
        container.arrow_btn = arrow_btn

        edit_btn = ctk.CTkButton(header_frame, text="Edit", width=40, fg_color=theme.COLOR_PRIMARY,
                                  command=lambda e=None: self._enter_edit_mode(container, task))
        edit_btn.pack(side="right", padx=5)

        details_frame = ctk.CTkFrame(container, fg_color="transparent")
        details_frame.pack(fill="x", padx=20, pady=(0,5))
        details_frame.pack_forget()
        container.details_frame = details_frame

        self._populate_details(details_frame, task)
        return container

    def _update_task_widget(self, task):
        container = self.task_widgets.get(task.id)
        if container is None:
            return
        if hasattr(container, "title_label"):
            container.title_label.configure(
                text=task.title,
                font=self.overstrike_font if task.done else self.normal_font,
                text_color="gray" if task.done else "white"
            )
        details_frame = container.details_frame
        for widget in details_frame.winfo_children():
            widget.destroy()
        self._populate_details(details_frame, task)

    def _populate_details(self, details_frame, task):
        details_lines = []
        if task.date:
            details_lines.append(f"Date: {task.date}")
        if task.time:
            details_lines.append(f"Time: {task.time}")
        if task.duration:
            details_lines.append(f"Duration: {task.duration} min")
        if details_lines:
            details_label = ctk.CTkLabel(details_frame, text="   ".join(details_lines), anchor="w", font=ctk.CTkFont(size=10))
            details_label.pack(fill="x")
        if task.description:
            desc_label = ctk.CTkLabel(details_frame, text=f"Description: {task.description}", anchor="w", font=ctk.CTkFont(size=10))
            desc_label.pack(fill="x", pady=(5,0))
        if task.subtasks:
            subtasks_text = "Subtasks: " + ", ".join([sub.title for sub in task.subtasks])
            subtasks_label = ctk.CTkLabel(details_frame, text=subtasks_text, anchor="w", font=ctk.CTkFont(size=10))
            subtasks_label.pack(fill="x", pady=(5,0))

    def _toggle_details(self, container):
        details = container.details_frame
        arrow_btn = container.arrow_btn
        if details.winfo_ismapped():
            details.pack_forget()
            arrow_btn.configure(text="►")
        else:
            details.pack(fill="x", padx=20, pady=(0,5))
            arrow_btn.configure(text="▼")

    def _edit_task_inline(self, task, title_label, header_frame):
        container = header_frame.master
        title_label.pack_forget()
        entry = ctk.CTkEntry(header_frame, width=200)
        entry.insert(0, task.title)
        entry.pack(side="left", padx=5, fill="x", expand=True)
        entry.focus()

        def save_edit(e=None):
            new_title = entry.get().strip()
            if new_title == "":
                new_title = task.title
            if new_title != task.title:
                task.title = new_title
                self.controller.update_task(task)
            entry.destroy()
            new_title_label = ctk.CTkLabel(header_frame, text=task.title, anchor="w",
                                            font=self.overstrike_font if task.done else self.normal_font,
                                            text_color="gray" if task.done else "white")
            new_title_label.pack(side="left", padx=5, fill="x", expand=True)
            new_title_label.bind("<Button-1>", lambda e: self._edit_task_inline(task, new_title_label, header_frame))
            container.title_label = new_title_label

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", save_edit)

    def _enter_edit_mode(self, container, task):
        details = container.details_frame
        if not details.winfo_ismapped():
            details.pack(fill="x", padx=20, pady=(0,5))
            container.arrow_btn.configure(text="▼")
        for widget in details.winfo_children():
            widget.destroy()

        date_label = ctk.CTkLabel(details, text="Date:", font=ctk.CTkFont(size=10))
        date_label.grid(row=0, column=0, sticky="w")
        date_entry = DateEntry(details, date_pattern="yyyy-mm-dd", width=10)
        if task.date:
            date_entry.set_date(task.date)
        date_entry.grid(row=0, column=1, sticky="w", padx=5)

        time_label = ctk.CTkLabel(details, text="Time:", font=ctk.CTkFont(size=10))
        time_label.grid(row=1, column=0, sticky="w")
        time_entry = ctk.CTkEntry(details, width=10, font=ctk.CTkFont(size=10))
        time_entry.insert(0, task.time if task.time else "")
        time_entry.grid(row=1, column=1, sticky="w", padx=5)

        duration_label = ctk.CTkLabel(details, text="Duration:", font=ctk.CTkFont(size=10))
        duration_label.grid(row=2, column=0, sticky="w")
        duration_entry = ctk.CTkEntry(details, width=10, font=ctk.CTkFont(size=10))
        duration_entry.insert(0, str(task.duration) if task.duration else "")
        duration_entry.grid(row=2, column=1, sticky="w", padx=5)

        desc_label = ctk.CTkLabel(details, text="Description:", font=ctk.CTkFont(size=10))
        desc_label.grid(row=3, column=0, sticky="w", pady=(5,0))
        desc_entry = ctk.CTkTextbox(details, width=250, height=60, font=ctk.CTkFont(size=10))
        desc_entry.insert("0.0", task.description if task.description else "")
        desc_entry.grid(row=4, column=0, columnspan=2, sticky="w", padx=5)

        subtask_header = ctk.CTkLabel(details, text="Subtasks:", font=ctk.CTkFont(size=10, weight="bold"))
        subtask_header.grid(row=5, column=0, sticky="w", pady=(10,0))
        row_index = 6
        for sub in task.subtasks:
            sub_frame = ctk.CTkFrame(details, fg_color="transparent")
            sub_frame.grid(row=row_index, column=0, columnspan=2, sticky="w", pady=2)
            sub_entry = ctk.CTkEntry(sub_frame, width=150, font=ctk.CTkFont(size=10))
            sub_entry.insert(0, sub.title)
            sub_entry.pack(side="left", padx=5)
            sub_entry.focus()
            sub_entry.bind("<Return>", lambda e, s=sub, entry=sub_entry: self._save_subtask_edit(s, entry, details))
            sub_entry.bind("<FocusOut>", lambda e, s=sub, entry=sub_entry: self._save_subtask_edit(s, entry, details))
            row_index += 1

        new_sub_entry = ctk.CTkEntry(details, placeholder_text="Add new subtask", font=ctk.CTkFont(size=10))
        new_sub_entry.grid(row=row_index, column=0, sticky="w", pady=(5,0))
        new_sub_entry.bind("<Return>", lambda e, entry=new_sub_entry: self._add_new_subtask(task, entry, details))
        new_sub_entry.bind("<FocusOut>", lambda e, entry=new_sub_entry: self._add_new_subtask(task, entry, details))
        row_index += 1

        save_btn = ctk.CTkButton(details, text="Save", command=lambda e=None: self._save_edits(task, date_entry, time_entry, duration_entry, desc_entry, container))
        save_btn.grid(row=row_index, column=0, columnspan=2, pady=5)

    def _save_subtask_edit(self, subtask, entry_widget, details):
        new_title = entry_widget.get().strip()
        if new_title and new_title != subtask.title:
            subtask.title = new_title
            self.controller.update_subtask(subtask)
        self._reload_edit_mode(details)

    def _add_new_subtask(self, task, entry_widget, details):
        title = entry_widget.get().strip()
        if title:
            self.controller.create_subtask(task.id, title=title)
        entry_widget.destroy()
        self._reload_edit_mode(details)

    def _reload_edit_mode(self, details):
        parent_container = details.master
        task = parent_container.task
        self._enter_edit_mode(parent_container, task)

    def _save_edits(self, task, date_entry, time_entry, duration_entry, desc_entry, container):
        task.date = date_entry.get_date().strftime("%Y-%m-%d")
        task.time = time_entry.get().strip()
        try:
            task.duration = int(duration_entry.get().strip())
        except ValueError:
            task.duration = None
        task.description = desc_entry.get("0.0", "end").strip()

        self.controller.update_task(task)
        container.details_frame.destroy()
        new_details = ctk.CTkFrame(container, fg_color="transparent")
        new_details.pack(fill="x", padx=20, pady=(0,5))
        container.details_frame = new_details
        self._populate_details(new_details, task)
        self.refresh_tasks()

    def _on_done_change(self, task_id, is_done):
        self.controller.mark_task_done(task_id, is_done)
        self.refresh_tasks()

    def _on_delete_task(self, task_id):
        self.controller.delete_task(task_id)
        self.refresh_tasks()

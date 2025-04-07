import customtkinter as ctk
from controllers.task_controller import list_tasks, update_task, delete_task, add_task
from models.task import Task
from views.edit_task_dialog import EditTaskDialog
from customtkinter import CTkFont


class MainView(ctk.CTkFrame):
    """Main view displaying tasks with inline editing capability and an example entry when no tasks exist."""
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(fg_color="transparent")
        self.create_widgets()

    def create_widgets(self):

        self.normal_font = CTkFont(family="Helvetica", size=12)
        self.overstrike_font = CTkFont(family="Helvetica", size=12, overstrike=1)

        self.title_label = ctk.CTkLabel(self, text="My Tasks", font=("Helvetica", 20))
        self.title_label.pack(pady=10)

        self.tasks_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.tasks_frame.pack(pady=5, fill="both", expand=True)

        self.add_button = ctk.CTkButton(self, text="+", width=40, command=self.open_inline_entry)
        self.add_button.pack(pady=5)
        self.refresh_tasks()

    def refresh_tasks(self):
        """Reload and display tasks; if none, show a clickable example label for adding a new task."""
        try:
            if not self.tasks_frame.winfo_exists():
                return
            for widget in self.tasks_frame.winfo_children():
                widget.destroy()
            self.tasks = list_tasks()
            if not self.tasks:
                self.open_example_task_entry()
            else:
                self.tasks.sort(key=lambda t: (t.done, -t.key if t.done else t.key))
                for task in self.tasks:
                    self.add_task_widget(task)
        except Exception as ex:
            print("Error in refresh_tasks:", ex)

    def open_example_task_entry(self):
        """
        Crée une ligne d'entrée pour ajouter une tâche quand la liste est vide.
        Cette ligne est insérée dans son propre conteneur, de sorte qu'elle ne perturbe pas le reste.
        """
        entry_frame = ctk.CTkFrame(self.tasks_frame, fg_color="#555555", corner_radius=8, height=40)
        entry_frame.pack(pady=10, padx=5, fill="x")
        entry_frame.pack_propagate(False)
        entry = ctk.CTkEntry(entry_frame, placeholder_text="New task title")
        entry.pack(side="left", padx=5, fill="x", expand=True)
        entry.focus()
        done_var = ctk.BooleanVar(value=False)
        checkbox = ctk.CTkCheckBox(entry_frame, variable=done_var, text="", width=25)
        checkbox.pack(side="left", padx=5)

        entry.bind("<Return>", lambda e: self.save_new_task(entry.get(), done_var.get(), entry_frame))
        entry.bind("<FocusOut>", lambda e: self.save_new_task(entry.get(), done_var.get(), entry_frame))

    def add_task_widget(self, task):
        """Create a row for a task with inline editable title."""
        row_frame = ctk.CTkFrame(self.tasks_frame, fg_color="transparent", corner_radius=8, height=40)
        row_frame.pack(pady=2, padx=5, fill="x")
        row_frame.pack_propagate(False)
        row_frame.bind("<Enter>", lambda e: row_frame.configure(cursor="hand2"))
        row_frame.bind("<Leave>", lambda e: row_frame.configure(cursor=""))

        has_details = bool(task.subtasks or task.description)
        if has_details:
            arrow_button = ctk.CTkButton(
                row_frame, text="►", width=25, fg_color="transparent", hover_color="#555555",
                command=lambda t=task: self.toggle_details(t, row_frame, arrow_button)
            )
            arrow_button.pack(side="right", padx=5)
        else:
            ctk.CTkLabel(row_frame, text="   ", width=25).pack(side="right", padx=5)

        done_var = ctk.BooleanVar(value=task.done)
        checkbox = ctk.CTkCheckBox(
            row_frame, variable=done_var, text="", width=25,
            command=lambda t=task, v=done_var: self.on_done_change(t, v.get())
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
        title_label = ctk.CTkLabel(row_frame, text=label_text, anchor="w", font=font_to_use, text_color=text_color)
        title_label.pack(side="left", padx=5, fill="x", expand=True)
        # On simple click, déclencher l'édition inline
        title_label.bind("<Button-1>", lambda e, t=task, lbl=title_label: self.edit_task_inline(t, lbl))
        
        edit_button = ctk.CTkButton(
            row_frame, text="✎", width=30, fg_color="blue", hover_color="#555555",
            command=lambda t=task: self.open_edit_popup(t)
        )
        edit_button.pack(side="right", padx=5)

        delete_button = ctk.CTkButton(
            row_frame, text="X", width=30, fg_color="red", hover_color="#aa0000",
            command=lambda t=task: self.delete_task(t)
        )
        delete_button.pack(side="right", padx=5)

    def edit_task_inline(self, task, label_widget):
        """Replace the task title label with an entry widget for inline editing."""
        label_widget.pack_forget()
        entry = ctk.CTkEntry(label_widget.master, width=200)
        entry.insert(0, task.title)
        entry.pack(side="left", padx=5, fill="x", expand=True)
        entry.focus()

        def save_edit(event=None):
            new_title = entry.get().strip()
            if new_title:
                task.title = new_title
                update_task(task)
            entry.destroy()
            details_str = ""
            if task.date:
                details_str += f" • {task.date}"
            if task.duration:
                details_str += f" • {task.duration} min"
            new_label_text = f"{task.title}{details_str}"
            if task.done:
                new_label_text = f"~~{new_label_text}~~"
            new_label = ctk.CTkLabel(label_widget.master, text=new_label_text, anchor="w", font=( "Helvetica", 12, "overstrike") if task.done else ("Helvetica", 12))
            new_label.pack(side="left", padx=5, fill="x", expand=True)
            new_label.bind("<Button-1>", lambda e, t=task, lbl=new_label: self.edit_task_inline(t, lbl))

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", save_edit)

    def on_done_change(self, task, done):
        task.done = done
        update_task(task)
        self.refresh_tasks()

    def toggle_details(self, task, parent_frame, arrow_button):
        """Toggle display of additional details (subtasks, description) for a task."""
        details_widget = getattr(parent_frame, "details_widget", None)
        if details_widget:
            details_widget.destroy()
            parent_frame.details_widget = None
            arrow_button.configure(text="►")
        else:
            details_text = ""
            if task.subtasks:
                for sub in task.subtasks:
                    details_text += f" - {sub}\n"
            if task.description:
                details_text += f"Note: {task.description}\n"
            details_widget = ctk.CTkLabel(parent_frame, text=details_text, anchor="w", fg_color="#222222")
            details_widget.pack(fill="x", padx=20, pady=2)
            parent_frame.details_widget = details_widget
            arrow_button.configure(text="▼")

    def delete_task(self, task):
        delete_task(task.key)
        self.refresh_tasks()

    def open_inline_entry(self):
        """Create an inline entry row to quickly add a new task."""
        if getattr(self, "task_entry_active", False):
            return
        self.task_entry_active = True

        entry_frame = ctk.CTkFrame(self.tasks_frame, fg_color="#555555", corner_radius=8, height=40)
        entry_frame.pack(pady=2, padx=5, fill="x")
        entry_frame.pack_propagate(False)

        entry = ctk.CTkEntry(entry_frame, placeholder_text="New task title")
        entry.pack(side="left", padx=5, fill="x", expand=True)
        entry.focus()

        done_var = ctk.BooleanVar(value=False)
        checkbox = ctk.CTkCheckBox(entry_frame, variable=done_var, text="", width=25)
        checkbox.pack(side="left", padx=5)

        def save_entry(event=None):
            if not self.task_entry_active:
                return
            self.task_entry_active = False
            self.save_new_task(entry.get(), done_var.get(), entry_frame)

        entry.bind("<Return>", save_entry)
        entry.bind("<FocusOut>", lambda e: self.after(100, save_entry))
        
    def save_new_task(self, title, done, container):
        if not title.strip():
            container.destroy()
            self.after(50, self.refresh_tasks)
            return
        new_task = Task(title=title, done=done)
        new_id = add_task(new_task)
        if new_id:
            new_task.key = new_id
            self.tasks.append(new_task)
            self.add_task_widget(new_task)
        container.destroy()
        self.after(50, self.refresh_tasks)

    def open_edit_popup(self, task):
        EditTaskDialog(self.master, task, self.refresh_tasks)

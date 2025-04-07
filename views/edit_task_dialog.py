import customtkinter as ctk
from tkcalendar import DateEntry
from controllers.task_controller import update_task, add_subtask, list_subtasks, delete_subtask, update_subtask
from models.subtask import Subtask
from customtkinter import CTkFont
import theme

class EditTaskDialog(ctk.CTkToplevel):
    """
    Modal dialog for editing task details, including subtasks.
    The dialog is scrollable and features a fixed footer with a Validate button.
    """
    def __init__(self, master, task, refresh_callback, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.task = task
        self.refresh_callback = refresh_callback
        self.title("Edit Task")
        self.geometry("400x600")

        # Make dialog modal and center it on the parent window
        self.transient(master)
        self.grab_set()
        self.center_window()
        self.lift()
        self.attributes("-topmost", True)
        self.after(10, lambda: self.attributes("-topmost", False))

        # Global container: scrollable content and fixed footer
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=380, height=500)
        self.scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.content_frame = self.scrollable_frame
        self.footer_frame = ctk.CTkFrame(self, height=50, fg_color="transparent")
        self.footer_frame.pack(fill="x", padx=10, pady=10)

        # Define fonts for subtasks
        self.normal_font = theme.get_font()
        self.overstrike_font = theme.get_font(overstrike=True)

        self.create_widgets()

    def center_window(self):
        """Center the dialog relative to the parent window."""
        self.update_idletasks()
        popup_width = self.winfo_width()
        popup_height = self.winfo_height()
        master = self.master
        master.update_idletasks()
        pos_x = master.winfo_rootx() + (master.winfo_width() - popup_width) // 2
        pos_y = master.winfo_rooty() + (master.winfo_height() - popup_height) // 2
        self.geometry(f"+{pos_x}+{pos_y}")

    def create_widgets(self):
        # Title field
        self.title_label = ctk.CTkLabel(self.content_frame, text="Title")
        self.title_label.pack(pady=(15,5))
        self.title_entry = ctk.CTkEntry(self.content_frame, width=300)
        self.title_entry.insert(0, self.task.title)
        self.title_entry.pack(pady=5)

        # Description field: multi-line textbox
        self.desc_label = ctk.CTkLabel(self.content_frame, text="Description")
        self.desc_label.pack(pady=(15,5))
        self.desc_textbox = ctk.CTkTextbox(self.content_frame, width=300, height=90)
        if self.task.description:
            self.desc_textbox.insert("0.0", self.task.description)
        self.desc_textbox.pack(pady=5)

        # Row for Date, Time and Duration (grouped on one line)
        dt_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        dt_frame.pack(pady=(15,5), fill="x", padx=5)
        dt_frame.grid_columnconfigure(0, weight=1)
        dt_frame.grid_columnconfigure(1, weight=1)
        dt_frame.grid_columnconfigure(2, weight=1)

        self.date_label = ctk.CTkLabel(dt_frame, text="Date")
        self.date_label.grid(row=0, column=0, padx=2)
        self.date_entry = DateEntry(dt_frame, date_pattern="yyyy-mm-dd", width=10)
        if self.task.date:
            self.date_entry.set_date(self.task.date)
        self.date_entry.grid(row=1, column=0, padx=2)

        self.time_label = ctk.CTkLabel(dt_frame, text="Time")
        self.time_label.grid(row=0, column=1, padx=2)
        time_options = [f"{h:02d}:{m:02d}" for h in range(0, 24) for m in (0, 15, 30, 45)]
        self.time_combobox = ctk.CTkComboBox(dt_frame, values=time_options, width=70)
        if self.task.time in time_options:
            self.time_combobox.set(self.task.time)
        else:
            self.time_combobox.set(time_options[0])
        self.time_combobox.grid(row=1, column=1, padx=2)

        self.duration_label = ctk.CTkLabel(dt_frame, text="Duration")
        self.duration_label.grid(row=0, column=2, padx=2)
        duration_options = [str(x) for x in (5, 10, 15, 20, 25, 30, 45, 60, 90, 120, 240, 480)]
        self.duration_combobox = ctk.CTkComboBox(dt_frame, values=duration_options, width=70)
        if self.task.duration and str(self.task.duration) in duration_options:
            self.duration_combobox.set(str(self.task.duration))
        else:
            self.duration_combobox.set(duration_options[0])
        self.duration_combobox.grid(row=1, column=2, padx=2)

        # --- Subtasks Section ---
        # Header with centered "Subtasks" label and inline add button on the right
        subtasks_header = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        subtasks_header.pack(pady=(15,5), fill="x", padx=5)
        subtasks_header.grid_columnconfigure(0, weight=1)
        subtasks_header.grid_columnconfigure(1, weight=2)
        subtasks_header.grid_columnconfigure(2, weight=1)
        self.subtasks_label = ctk.CTkLabel(subtasks_header, text="Subtasks", font=self.normal_font)
        self.subtasks_label.grid(row=0, column=1, sticky="nsew")
        self.inline_add_subtask_button = ctk.CTkButton(subtasks_header, text="+", width=30, fg_color="blue",
                                                       command=self.open_add_subtask_entry)
        self.inline_add_subtask_button.grid(row=0, column=2, sticky="e", padx=5)

        # Scrollable container for subtasks
        self.subtasks_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.subtasks_container.pack(pady=5, fill="both", expand=False)
        self.update_subtasks_list()

        # Footer: Validate button fixed
        self.validate_button = ctk.CTkButton(self.footer_frame, text="Validate", command=self.save_changes)
        self.validate_button.pack(side="right", padx=5, pady=5)

    def update_subtasks_list(self):
        """Refresh the list of subtasks in the scrollable container."""
        for widget in self.subtasks_container.winfo_children():
            widget.destroy()
        from controllers.task_controller import list_subtasks
        self.task.subtasks = list_subtasks(self.task.key)
        if not self.task.subtasks:
            # Display an example label that is clickable
            example_label = ctk.CTkLabel(self.subtasks_container, text="Click here to add a subtask",
                                          text_color="gray", anchor="center")
            example_label.pack(pady=10, fill="x")
            example_label.bind("<Button-1>", lambda e: self.edit_example_subtask(example_label))
        else:
            self.task.subtasks.sort(key=lambda s: (s.done, -s.key if s.done else s.key))
            for sub in self.task.subtasks:
                sub_frame = ctk.CTkFrame(self.subtasks_container, fg_color="transparent")
                sub_frame.pack(fill="x", padx=5, pady=2)
                done_var = ctk.BooleanVar(value=sub.done)
                sub_checkbox = ctk.CTkCheckBox(sub_frame, variable=done_var, text="", width=20,
                                               command=lambda s=sub, v=done_var: self.update_subtask_done(s, v.get()))
                sub_checkbox.pack(side="left", padx=5)
                font_to_use = self.overstrike_font if sub.done else self.normal_font
                text_color = "gray" if sub.done else None
                sub_label = ctk.CTkLabel(sub_frame, text=sub.title, anchor="w", font=font_to_use, text_color=text_color)
                sub_label.pack(side="left", fill="x", expand=True)
                sub_label.bind("<Button-1>", lambda e, s=sub, f=sub_frame: self.edit_subtask_inline(s, f))
                del_button = ctk.CTkButton(sub_frame, text="X", width=25, fg_color="red",
                                           command=lambda s=sub: self.delete_subtask(s))
                del_button.pack(side="right", padx=5)

    def update_subtask_done(self, subtask, done):
        subtask.done = done
        from controllers.task_controller import update_subtask
        update_subtask(subtask)
        self.update_subtasks_list()

    def edit_example_subtask(self, example_label):
        """
        Replace the example label with an inline Entry widget to add a new subtask in place.
        """
        container = example_label.master
        example_label.destroy()
        entry = ctk.CTkEntry(container, placeholder_text="New subtask title")
        entry.pack(fill="x", padx=5, pady=5)
        entry.focus()
        entry.bind("<Return>", lambda e: self.save_new_subtask_inline(entry, container))
        entry.bind("<FocusOut>", lambda e: self.save_new_subtask_inline(entry, container))

    def save_new_subtask_inline(self, entry, container):
        title = entry.get().strip()
        entry.destroy()
        if title:
            from controllers.task_controller import add_subtask
            new_sub = Subtask(task_key=self.task.key, title=title)
            new_id = add_subtask(new_sub)
            if new_id:
                new_sub.key = new_id
        self.update_subtasks_list()

    def edit_subtask_inline(self, subtask, container_frame):
        """Enable inline editing of a subtask's title."""
        for widget in container_frame.winfo_children():
            widget.destroy()
        edit_entry = ctk.CTkEntry(container_frame, width=200)
        edit_entry.insert(0, subtask.title)
        edit_entry.pack(side="left", padx=5, fill="x", expand=True)
        edit_entry.focus()

        def save_edit(event=None):
            new_title = edit_entry.get().strip()
            if new_title:
                subtask.title = new_title
                from controllers.task_controller import update_subtask
                update_subtask(subtask)
            self.update_subtasks_list()

        edit_entry.bind("<Return>", save_edit)
        edit_entry.bind("<FocusOut>", save_edit)

    def open_add_subtask_entry(self):
        """Open an inline entry to add a new subtask."""
        entry_frame = ctk.CTkFrame(self.subtasks_container, fg_color="#555555", corner_radius=8)
        entry_frame.pack(pady=2, padx=5, fill="x")
        entry = ctk.CTkEntry(entry_frame, placeholder_text="New subtask title")
        entry.pack(side="left", padx=5, fill="x", expand=True)
        entry.focus()
        entry.bind("<Return>", lambda e: self.save_new_subtask(entry.get(), entry_frame))
        entry.bind("<FocusOut>", lambda e: self.save_new_subtask(entry.get(), entry_frame))

    def save_new_subtask(self, title, entry_frame):
        """Save a new subtask if the title is not empty, then update the list."""
        if not title.strip():
            entry_frame.destroy()
            return
        from controllers.task_controller import add_subtask
        new_sub = Subtask(task_key=self.task.key, title=title.strip())
        new_id = add_subtask(new_sub)
        if new_id:
            new_sub.key = new_id
            self.update_subtasks_list()
        entry_frame.destroy()

    def delete_subtask(self, subtask):
        """Delete a subtask and refresh the list."""
        from controllers.task_controller import delete_subtask
        delete_subtask(subtask.key)
        self.update_subtasks_list()

    def save_changes(self, event=None):
        """Save all changes made in the dialog."""
        self.task.title = self.title_entry.get()
        self.task.description = self.desc_textbox.get("0.0", "end").strip()
        self.task.date = self.date_entry.get_date().strftime("%Y-%m-%d")
        self.task.time = self.time_combobox.get()
        try:
            self.task.duration = int(self.duration_combobox.get())
        except ValueError:
            self.task.duration = None
        from controllers.task_controller import update_task
        update_task(self.task)
        self.refresh_callback()
        self.destroy()

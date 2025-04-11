"""
tasks_table_header.py

TasksTableHeader renders the header for the tasks table, including column labels
for Title, Project, Status, Priority, Due Date, Last Update, and buttons for filtering
and selecting all or deleting selected tasks. It uses common grid configuration settings.

Constants like HEADER_HEIGHT and SEPARATOR_COLOR are defined here, along with placeholder
filters for demonstration.
"""

import customtkinter as ctk
from theme import get_font, current_mode, load_icon
from components.grid_config import COMMON_GRID_CONFIG

HEADER_HEIGHT = 40
SEPARATOR_COLOR = "#CCCCCC"  # Color for vertical separators.

# Placeholder filter options (replace with dynamic values as needed).
FILTER_PROJECTS = ["Project A", "Project B", "Project C"]
FILTER_STATUSES = ["Not Started", "In Progress", "Completed"]
FILTER_PRIORITIES = ["Low", "Medium", "High"]

class TasksTableHeader(ctk.CTkFrame):
    def __init__(self, master, on_select_all, on_delete_selected, on_filter_sort_change, *args, **kwargs):
        """
        Initialize the TasksTableHeader.

        Args:
            master: Parent widget.
            on_select_all (callable): Callback when the global checkbox is toggled.
            on_delete_selected (callable): Callback when deleting selected tasks.
            on_filter_sort_change (callable): Callback when a sort/filter option is changed.
            *args, **kwargs: Additional arguments.
        """
        super().__init__(master, *args, **kwargs)
        self.configure(fg_color="transparent", height=HEADER_HEIGHT)
        self.on_select_all = on_select_all
        self.on_delete_selected = on_delete_selected
        self.on_filter_sort_change = on_filter_sort_change

        # Maintain sorting state for columns.
        self.sort_states = {
            "title": None,
            "project": None,
            "status": None,
            "priority": None,
            "due_date": None,
            "updated": None
        }
        self.current_sort_field = None
        self.base_texts = {
            "title": "Title",
            "project": "Project",
            "status": "Status",
            "priority": "Priority",
            "due_date": "Due Date",
            "updated": "Last Update"
        }

        # Configure the grid columns using the common grid configuration.
        for col, conf in COMMON_GRID_CONFIG.items():
            self.grid_columnconfigure(col, **conf)

        self._create_widgets()
        self._add_horizontal_separator()

    def _create_widgets(self):
        """
        Creates and positions all header widgets for the table.
        """
        # Column 0: Global checkbox.
        self.select_all_var = ctk.BooleanVar(value=False)
        self.select_all_cb = ctk.CTkCheckBox(
            self,
            variable=self.select_all_var,
            command=lambda: self.on_select_all(self.select_all_var.get()),
            text="",
            width=30
        )
        self.select_all_cb.grid(row=0, column=0, padx=0, pady=2, sticky="w")

        # Column 1: Vertical separator.
        self._add_separator(col=1)

        # Column 2: Title label.
        self.title_label = ctk.CTkLabel(
            self,
            text=self.base_texts["title"],
            font=get_font("button"),
            anchor="center"
        )
        self.title_label.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        self.title_label.bind("<Button-1>", lambda e: self._toggle_sort("title"))

        # Column 3: Separator.
        self._add_separator(col=3)

        # Column 4: Project label.
        self.project_label = ctk.CTkLabel(
            self,
            text=self.base_texts["project"],
            font=get_font("button"),
            anchor="center"
        )
        self.project_label.grid(row=0, column=4, padx=5, pady=5, sticky="nsew")
        self.project_label.bind("<Button-1>", lambda e: self._toggle_sort("project"))

        # Column 5: Separator.
        self._add_separator(col=5)

        # Column 6: Status label.
        self.status_label = ctk.CTkLabel(
            self,
            text=self.base_texts["status"],
            font=get_font("button"),
            anchor="center"
        )
        self.status_label.grid(row=0, column=6, padx=5, pady=5, sticky="nsew")
        self.status_label.bind("<Button-1>", lambda e: self._toggle_sort("status"))

        # Column 7: Separator.
        self._add_separator(col=7)

        # Column 8: Priority label.
        self.priority_label = ctk.CTkLabel(
            self,
            text=self.base_texts["priority"],
            font=get_font("button"),
            anchor="center"
        )
        self.priority_label.grid(row=0, column=8, padx=5, pady=5, sticky="nsew")
        self.priority_label.bind("<Button-1>", lambda e: self._toggle_sort("priority"))

        # Column 9: Separator.
        self._add_separator(col=9)

        # Column 10: Due Date label.
        self.duedate_label = ctk.CTkLabel(
            self,
            text=self.base_texts["due_date"],
            font=get_font("button"),
            anchor="center"
        )
        self.duedate_label.grid(row=0, column=10, padx=5, pady=5, sticky="nsew")
        self.duedate_label.bind("<Button-1>", lambda e: self._toggle_sort("due_date"))

        # Column 11: Separator.
        self._add_separator(col=11)

        # Column 12: Last Update label.
        self.updated_label = ctk.CTkLabel(
            self,
            text=self.base_texts["updated"],
            font=get_font("button"),
            anchor="center"
        )
        self.updated_label.grid(row=0, column=12, padx=5, pady=5, sticky="nsew")
        self.updated_label.bind("<Button-1>", lambda e: self._toggle_sort("updated"))

        # Column 13: Global filter button.
        dark_mode = (current_mode == "dark")
        filter_icon = ctk.CTkImage(load_icon("icons/logout.png", size=(15, 15), invert=dark_mode), size=(15, 15))
        self.filter_btn = ctk.CTkButton(
            self,
            text="",
            image=filter_icon,
            command=self._open_filter_menu,
            width=20,
            height=20,
            fg_color="transparent"
        )
        self.filter_btn.grid(row=0, column=13, padx=5, pady=5, sticky="e")

        # Column 14: "Delete Selected" button.
        small_font = get_font("button", size=int(get_font("button", size=18).cget("size")/2))
        self.delete_selected_btn = ctk.CTkButton(
            self,
            text="Delete\nSelected",
            fg_color="#D9534F",
            command=self.on_delete_selected,
            font=small_font,
            width=40,
            height=40
        )
        self.delete_selected_btn.grid(row=0, column=14, padx=(10, 10), pady=5, sticky="e")

    def _add_separator(self, col: int):
        """
        Adds a vertical separator at the specified column.

        Args:
            col (int): Column number where the separator should be added.
        """
        sep = ctk.CTkFrame(
            self,
            width=1,
            height=HEADER_HEIGHT - 10,
            fg_color=SEPARATOR_COLOR,
            bg_color=SEPARATOR_COLOR
        )
        sep.grid(row=0, column=col, padx=0)

    def _add_horizontal_separator(self):
        """
        Adds a horizontal separator below the header.
        """
        sep = ctk.CTkFrame(self, height=1, fg_color=SEPARATOR_COLOR, bg_color=SEPARATOR_COLOR)
        sep.grid(row=1, column=0, columnspan=15, padx=0, pady=(5, 10), sticky="ew")

    def _toggle_sort(self, field: str):
        """
        Toggles the sort state for a given column field and triggers the filter/sort callback.

        Args:
            field (str): The column field to sort by.
        """
        if self.current_sort_field and self.current_sort_field != field:
            self.sort_states[self.current_sort_field] = None
            self._reset_sort_label(self.current_sort_field)
            self.current_sort_field = None

        current = self.sort_states.get(field)
        if current is None or current == "desc":
            new_state = "asc"
            arrow = " ▲"
        else:
            new_state = "desc"
            arrow = " ▼"
        self.sort_states[field] = new_state
        self.current_sort_field = field
        new_text = self.base_texts[field] + arrow

        if field == "title":
            self.title_label.configure(text=new_text)
        elif field == "project":
            self.project_label.configure(text=new_text)
        elif field == "status":
            self.status_label.configure(text=new_text)
        elif field == "priority":
            self.priority_label.configure(text=new_text)
        elif field == "due_date":
            self.duedate_label.configure(text=new_text)
        elif field == "updated":
            self.updated_label.configure(text=new_text)
        self.on_filter_sort_change(field, f"Sort {new_state}")

    def _reset_sort_label(self, field: str):
        """
        Resets the label text for a given field to its base value.

        Args:
            field (str): The field for which to reset the label.
        """
        base = self.base_texts[field]
        if field == "title":
            self.title_label.configure(text=base)
        elif field == "project":
            self.project_label.configure(text=base)
        elif field == "status":
            self.status_label.configure(text=base)
        elif field == "priority":
            self.priority_label.configure(text=base)
        elif field == "due_date":
            self.duedate_label.configure(text=base)
        elif field == "updated":
            self.updated_label.configure(text=base)

    def _open_filter_menu(self):
        """
        Opens a pop-up filter menu for selecting filter options.
        """
        popup = ctk.CTkToplevel(self)
        popup.geometry("220x300")
        popup.title("")
        popup.overrideredirect(True)
        x = self.winfo_rootx() + self.filter_btn.winfo_x()
        y = self.winfo_rooty() + self.filter_btn.winfo_y() + self.filter_btn.winfo_height()
        popup.geometry(f"+{x}+{y}")

        proj_label = ctk.CTkLabel(popup, text="Filter by Project", font=get_font("button"))
        proj_label.pack(pady=(5, 0))
        for proj in FILTER_PROJECTS:
            btn = ctk.CTkButton(popup, text=proj, font=get_font("button"), width=180,
                                command=lambda p=proj: self._select_filter("project", p, popup))
            btn.pack(pady=2)
        
        status_label = ctk.CTkLabel(popup, text="Filter by Status", font=get_font("button"))
        status_label.pack(pady=(10, 0))
        for status in FILTER_STATUSES:
            btn = ctk.CTkButton(popup, text=status, font=get_font("button"), width=180,
                                command=lambda s=status: self._select_filter("status", s, popup))
            btn.pack(pady=2)
        
        priority_label = ctk.CTkLabel(popup, text="Filter by Priority", font=get_font("button"))
        priority_label.pack(pady=(10, 0))
        for prio in FILTER_PRIORITIES:
            btn = ctk.CTkButton(popup, text=prio, font=get_font("button"), width=180,
                                command=lambda p=prio: self._select_filter("priority", p, popup))
            btn.pack(pady=2)
        
        clear_btn = ctk.CTkButton(popup, text="Clear Filter", font=get_font("button"), width=180,
                                  command=lambda: self._select_filter("filter", "None", popup))
        clear_btn.pack(pady=(10, 5))

    def _select_filter(self, field: str, option: str, popup):
        """
        Applies the selected filter option and closes the filter menu.

        Args:
            field (str): The field being filtered.
            option (str): The chosen filter option.
            popup: The filter menu pop-up window.
        """
        self.on_filter_sort_change(field, option)
        popup.destroy()

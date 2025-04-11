# TDL (To Do List) Application v0.07

## Introduction

TDL is an evolving To Do List application developed in Python. Version 0.07 is a major step in its evolution after an initial prototype in v0.01. The project has been continuously improved to deliver a modular and well-structured architecture by clearly separating the logic of views, controllers, and models.

## Features

- **Task and Project Management**: Create, update, delete, and view tasks and subtasks, along with related projects.
- **Flexible and Sleek Interface**: Built on CustomTkinter with centralized theme and translation management to ensure a consistent UI.
- **Animated Sidebar Navigation**: An animated sidebar provides smooth navigation between different views (tasks, calendar, dashboard, settings, etc.).
- **Data Export**: Export your tasks in CSV and JSON formats for compatibility with other tools.
- **Evolving Architecture**: Designed with a modular approach, enabling easy updates and future extensions through a common base class for views.

## Installation

### Prerequisites

- Python 3.10 or later
- SQLite3 (comes bundled with Python)

**Required Python packages:**
- `customtkinter`
- `tkcalendar`
- `Pillow`

(Additional packages might be specified in the `requirements.txt` if available)

## Installation Instructions

### Clone the repository:
```bash
git clone https://github.com/Lahoucine-7/TDL.git
cd TDL
```

### Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate      # On Linux or macOS
venv\Scripts\activate         # On Windows
```

### Install dependencies:
```bash
pip install -r requirements.txt
```
(Si vous n'avez pas un fichier requirements.txt, installez manuellement `customtkinter`, `tkcalendar`, `Pillow`, etc.)

### Initialize the database:
The application automatically initializes the database on startup by calling `init_db()` from `database/database.py`.

## Usage

To run the application, execute the `app.py` file:
```bash
python app.py
```
The interface is composed of a sidebar for navigation and a main container that loads the corresponding view (tasks, calendar, dashboard, settings, etc.).

## Architecture

The code is organized into several folders to separate responsibilities:
- `models/` – Defines data classes for tasks, projects, users, etc.
- `controllers/` – Business logic handling CRUD operations for each model.
- `views/` – User interface components built with CustomTkinter that display and allow interaction with the data.
- `components/` – Reusable components such as task rows, task details, grid configuration, etc.
- `database/` – Manages database connections and table creation.

## Contributing

Contributions are welcome! If you have ideas for improvements, bug fixes, or new features, please feel free to open an issue or submit a pull request on the GitHub repository.

## Future Improvements

- Further refactor the UI for enhanced responsiveness and accessibility.
- Add new features such as reminders or integration with external services.
- Improve error handling and add unit tests.


## Acknowledgments

Thanks to the developers of CustomTkinter, tkcalendar, and Pillow for their great work, which made it possible to create this application.

# TDL (To Do List) Application v0.07

## Introduction / Introduction

### French:
TDL est une application To Do List évolutive développée en Python. La version 0.07 représente une étape significative dans son évolution, après un premier prototype en v0.01. Ce projet a été continuellement amélioré pour offrir une architecture modulaire et bien structurée, en séparant clairement la logique des vues, des contrôleurs et des modèles.

### English:
TDL is an evolving To Do List application developed in Python. Version 0.07 is a major step in its evolution after an initial prototype in v0.01. The project has been continuously improved to deliver a modular and well-structured architecture by clearly separating the logic of views, controllers, and models.

## Features / Fonctionnalités

### French:
- **Gestion des tâches et projets** : Créez, modifiez, supprimez et visualisez des tâches ainsi que leurs sous-tâches, ainsi que des projets associés.
- **Interface modulable et élégante** : Utilise CustomTkinter avec une gestion centralisée des thèmes et de la traduction pour garantir une interface cohérente.
- **Animation de la barre latérale** : Une sidebar animée facilite la navigation entre les différentes vues (tâches, calendrier, dashboard, réglages, etc.).
- **Export des données** : Exportez vos tâches au format CSV et JSON pour une compatibilité avec d'autres outils.
- **Architecture évolutive** : Le projet a été structuré pour permettre des mises à jour faciles et une extension future, en utilisant notamment une classe de base partagée entre les vues.

### English:
- **Task and Project Management**: Create, update, delete, and view tasks and subtasks, along with related projects.
- **Flexible and Sleek Interface**: Built on CustomTkinter with centralized theme and translation management to ensure a consistent UI.
- **Animated Sidebar Navigation**: An animated sidebar provides smooth navigation between different views (tasks, calendar, dashboard, settings, etc.).
- **Data Export**: Export your tasks in CSV and JSON formats for compatibility with other tools.
- **Evolving Architecture**: Designed with a modular approach, enabling easy updates and future extensions through a common base class for views.

## Installation / Installation

### Prérequis / Prerequisites

- Python 3.10 or later
- SQLite3 (comes bundled with Python)

**Required Python packages:**
- `customtkinter`
- `tkcalendar`
- `Pillow`

(Additional packages might be specified in the `requirements.txt` if available)

## Instructions d'installation / Installation Instructions

### Clonez le repository / Clone the repository:
```bash
git clone https://github.com/Lahoucine-7/TDL.git
cd TDL
```

### Créez et activez un environnement virtuel (optionnel mais recommandé) / Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate      # On Linux or macOS
venv\Scripts\activate         # On Windows
```

### Installez les dépendances / Install dependencies:
```bash
pip install -r requirements.txt
```
(Si vous n'avez pas un fichier requirements.txt, installez manuellement `customtkinter`, `tkcalendar`, `Pillow`, etc.)

### Initialisez la base de données / Initialize the database:
The application automatically initializes the database on startup by calling `init_db()` from `database/database.py`.

## Usage / Utilisation

### French:
Pour lancer l'application, exécutez le fichier `app.py` :
```bash
python app.py
```
L'interface se compose d'une sidebar pour naviguer entre les vues et d'un conteneur principal qui charge la vue correspondante (tâches, calendrier, dashboard, réglages, etc.).

### English:
To run the application, execute the `app.py` file:
```bash
python app.py
```
The interface is composed of a sidebar for navigation and a main container that loads the corresponding view (tasks, calendar, dashboard, settings, etc.).

## Architecture / Architecture

### French:
Le code est organisé en plusieurs dossiers pour séparer les responsabilités :
- `models/` – Définition des classes de données pour les tâches, projets, utilisateurs, etc.
- `controllers/` – Logique métier pour gérer les opérations CRUD (création, lecture, mise à jour, suppression) pour chaque modèle.
- `views/` – Composants d’interface utilisateur, en utilisant CustomTkinter, qui affichent et permettent l’interaction avec les données.
- `components/` – Composants réutilisables tels que les lignes du tableau de tâches, les détails de la tâche, la configuration de la grille, etc.
- `database/` – Gestion de la connexion à la base de données et création de tables.

### English:
The code is organized into several folders to separate responsibilities:
- `models/` – Defines data classes for tasks, projects, users, etc.
- `controllers/` – Business logic handling CRUD operations for each model.
- `views/` – User interface components built with CustomTkinter that display and allow interaction with the data.
- `components/` – Reusable components such as task rows, task details, grid configuration, etc.
- `database/` – Manages database connections and table creation.

## Contributing / Contribuer

### French:
Toute contribution est la bienvenue ! Si vous avez des idées d'amélioration, des corrections ou de nouvelles fonctionnalités à proposer, n'hésitez pas à créer une issue ou à soumettre une pull request sur le repository GitHub.

### English:
Contributions are welcome! If you have ideas for improvements, bug fixes, or new features, please feel free to open an issue or submit a pull request on the GitHub repository.

## Future Improvements / Améliorations Futures

### French:
- Refactor further parts of the UI for responsiveness and accessibility.
- Ajouter de nouvelles fonctionnalités telles que des rappels ou l'intégration avec d'autres services.
- Améliorer la gestion des erreurs et ajouter des tests unitaires.

### English:
- Further refactor the UI for enhanced responsiveness and accessibility.
- Add new features such as reminders or integration with external services.
- Improve error handling and add unit tests.


## Acknowledgments / Remerciements

### French:
Merci aux développeurs des librairies CustomTkinter, tkcalendar, et Pillow pour leur excellent travail qui a facilité la création de cette application.

### English:
Thanks to the developers of CustomTkinter, tkcalendar, and Pillow for their great work, which made it possible to create this application.

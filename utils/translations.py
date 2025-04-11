"""
translations.py

Manages string translations for the application.
Supports multiple languages using a dictionary.
"""

# Translation dictionaries for supported languages.
TRANSLATIONS = {
    "en": {
         "dashboard": "Dashboard",
         "calendar": "Calendar",
         "tasks": "Tasks",
         "projects": "Projects",
         "settings": "Settings",
         "project": "Project Detail",
         "share": "Share",
         "login": "Log in",
         "logout": "Log out",
         "search_placeholder": "Search",
         "menu": "Menu",
         "no_projects": "No projects. Click to add.",
         "toggle_theme": "Toggle Theme",
         "select_font": "Select Font",
         "show_tasks": "Show Tasks",
         "no_tasks_for_date": "No tasks for this date.",
         "total_tasks": "Total Tasks:",
         "completed_tasks": "Completed Tasks:",
         "overdue_tasks": "Overdue Tasks:",
         "total_projects": "Total Projects:",
         "add_project": "Add Project",
         "no_description": "No description",
         "confirm_deletion": "Confirm deletion",
         "delete_project_msg": "Delete project and ALL associated tasks?",
         "yes_delete_all": "Click Yes to delete project with its tasks.",
         "no_keep_tasks": "Click No to delete project and KEEP tasks.",
         "cancel": "Click Cancel to abort.",
         "project_name": "Project Name",
         "create": "Create"
    },
    "fr": {
         "dashboard": "Tableau de bord",
         "calendar": "Calendrier",
         "tasks": "Tâches",
         "projects": "Projets",
         "settings": "Réglages",
         "project": "Détail du projet",
         "share": "Partager",
         "login": "Se connecter",
         "logout": "Se déconnecter",
         "search_placeholder": "Recherche",
         "menu": "Menu",
         "no_projects": "Cliquez ici pour créer un projet.",
         "toggle_theme": "Changer le thème",
         "select_font": "Sélectionner la police",
         "show_tasks": "Afficher les tâches",
         "no_tasks_for_date": "Aucune tâche pour cette date.",
         "total_tasks": "Total des tâches:",
         "completed_tasks": "Tâches terminées:",
         "overdue_tasks": "Tâches en retard:",
         "total_projects": "Total des projets:",
         "add_project": "Ajouter un projet",
         "no_description": "Pas de description",
         "confirm_deletion": "Confirmer la suppression",
         "delete_project_msg": "Supprimer le projet et TOUTES les tâches associées?",
         "yes_delete_all": "Cliquez sur Oui pour supprimer le projet avec ses tâches.",
         "no_keep_tasks": "Cliquez sur Non pour supprimer le projet et GARDER les tâches.",
         "cancel": "Cliquez sur Annuler pour interrompre.",
         "project_name": "Nom du projet",
         "create": "Créer"
    }
}

class TranslationsManager:
    """
    Manages application translations. Provides a simple way to retrieve
    translated strings based on the current language.
    """
    def __init__(self, language="en"):
        self.set_language(language)

    def set_language(self, language: str):
        """
        Sets the current language. If the language is unsupported,
        defaults to English.
        
        Args:
            language (str): Language code ("en", "fr", etc.).
        """
        if language not in TRANSLATIONS:
            language = "en"
        self.language = language
        self.translations = TRANSLATIONS[language]

    def t(self, key: str) -> str:
        """
        Retrieve the translation for the specified key.
        
        Args:
            key (str): The translation key.
        Returns:
            str: The translated string or the key if not found.
        """
        return self.translations.get(key, key)

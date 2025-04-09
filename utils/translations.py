# utils/translations.py

# Dictionnaires de traduction pour chaque langue disponible
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
         "menu": "Menu"
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
         "menu": "Menu"
    }
}

class TranslationsManager:
    """
    Gestionnaire de traductions.
    
    Permet de récupérer les textes traduits selon la langue active.
    """
    def __init__(self, language="en"):
        self.set_language(language)

    def set_language(self, language):
        # On passe à l'anglais si la langue demandée n'est pas supportée
        if language not in TRANSLATIONS:
            language = "en"
        self.language = language
        self.translations = TRANSLATIONS[language]

    def t(self, key):
        """
        Retourne la traduction correspondant à la clé,
        ou la clé elle-même si la traduction n'est pas trouvée.
        """
        return self.translations.get(key, key)

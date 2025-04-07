# theme.py
import customtkinter as ctk

# Liste de polices disponibles (adapter selon vos besoins)
AVAILABLE_FONTS = ["Helvetica", "Roboto", "Inter", "Poppins"]

# Valeurs par défaut
DEFAULT_FONT_FAMILY = "Helvetica"
DEFAULT_FONT_SIZE = 12

# Exemple de palette de couleurs
COLOR_PRIMARY = "#1F6AA5"
COLOR_SECONDARY = "#13293D"
COLOR_ACCENT = "#EA6F5A"

def get_font(family=None, size=None, overstrike=False):
    """
    Crée et renvoie un CTkFont selon les paramètres choisis.
    :param family: Nom de la police. Par défaut = DEFAULT_FONT_FAMILY
    :param size: Taille de la police. Par défaut = DEFAULT_FONT_SIZE
    :param overstrike: Booléen indiquant si le texte doit être barré
    :return: CTkFont
    """
    family = family or DEFAULT_FONT_FAMILY
    size = size or DEFAULT_FONT_SIZE
    return ctk.CTkFont(family=family, size=size, overstrike=overstrike)
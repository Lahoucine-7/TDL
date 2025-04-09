import json
import customtkinter as ctk
from customtkinter import ThemeManager
from PIL import Image, ImageOps

DEFAULT_THEME_PATH = "my_theme.json"

# Paramètres utilisateur par défaut
current_mode = "dark"        # "dark" ou "light"
current_palette = "default"  # Options : "default", "blue", ou "green"
available_fonts = ["Roboto", "Helvetica", "Inter"]
current_font = "Roboto"
font_size_presets = {
    "small": {"title": 24, "subtitle": 18, "text": 12, "button": 14, "label": 12},
    "medium": {"title": 28, "subtitle": 20, "text": 14, "button": 16, "label": 14},
    "large": {"title": 32, "subtitle": 24, "text": 18, "button": 20, "label": 18}
}
current_size_preset = "medium"

def merge_dict(default, custom):
    """Fusionne récursivement 'custom' dans 'default'."""
    for key, value in custom.items():
        if key in default and isinstance(default[key], dict) and isinstance(value, dict):
            merge_dict(default[key], value)
        else:
            default[key] = value
    return default

def load_theme(path=DEFAULT_THEME_PATH):
    """
    Charge le thème personnalisé et le fusionne avec le thème par défaut.
    Met ensuite à jour ThemeManager.theme.
    """
    with open(path, "r") as f:
        custom_theme = json.load(f)
    default_theme = ThemeManager.theme.copy()
    merged_theme = merge_dict(default_theme, custom_theme)
    palettes = merged_theme.get("palettes", {})
    palette_config = palettes.get(current_palette, {}).get(current_mode, {})
    merged_theme = merge_dict(merged_theme, palette_config)
    ThemeManager.theme = merged_theme

load_theme()

def get_font(style=None, family=None, size=None, overstrike=False):
    """
    Renvoie un objet CTkFont configuré en fonction du style et de la taille.
    """
    if not family:
        family = current_font
    if style and not size:
        fonts_config = ThemeManager.theme.get("fonts", {})
        style_config = fonts_config.get("styles", {}).get(style, {})
        size_key = style_config.get("size", "medium")
        size = fonts_config.get("sizes", {}).get(size_key, 18)
    if not size:
        size = 18
    return ctk.CTkFont(family=family, size=size, overstrike=overstrike)

def get_default_frame_color():
    """Renvoie la couleur de fond par défaut pour un CTkFrame."""
    return ThemeManager.theme.get("CTk", {}).get("bg_color", "#08090D")

def get_ctkframe_top_color():
    """
    Renvoie la valeur de 'top_fg_color' pour CTkFrame depuis le thème.
    """
    return ThemeManager.theme.get("CTkFrame", {}).get("top_fg_color", "#08090D")

def load_icon(path, size=(30,30), invert=False):
    """
    Charge et redimensionne une icône.
    Si 'invert' est True, inverse les couleurs RGB tout en conservant le canal alpha.
    """
    image = Image.open(path).convert("RGBA")
    if invert:
        r, g, b, a = image.split()
        rgb_image = Image.merge("RGB", (r, g, b))
        inverted_rgb = ImageOps.invert(rgb_image)
        image = Image.merge("RGBA", (*inverted_rgb.split(), a))
    return image.resize(size, Image.LANCZOS)

def set_mode(new_mode):
    global current_mode
    if new_mode in ["dark", "light"]:
        current_mode = new_mode
        load_theme(DEFAULT_THEME_PATH)

def set_palette(new_palette):
    global current_palette
    if new_palette in ThemeManager.theme.get("palettes", {}):
        current_palette = new_palette
        load_theme(DEFAULT_THEME_PATH)

def set_font(new_font):
    global current_font
    if new_font in available_fonts:
        current_font = new_font

def set_size_preset(new_preset):
    global current_size_preset
    if new_preset in font_size_presets:
        current_size_preset = new_preset

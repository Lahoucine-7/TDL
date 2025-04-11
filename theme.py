"""
theme.py

This module manages theme configuration for the application. It loads and merges a custom theme JSON file
with the default CustomTkinter theme. The module also provides helper functions to retrieve fonts, colors,
and images for the UI.
"""

import json
import logging
import customtkinter as ctk
from customtkinter import ThemeManager
from PIL import Image, ImageOps

# Theme configuration constants
DEFAULT_THEME_PATH = "my_theme.json"
current_mode = "dark"        # "dark" or "light"
current_palette = "default"  # Options: "default", "blue", or "green"
available_fonts = ["Roboto", "Helvetica", "Inter"]
current_font = "Roboto"
font_size_presets = {
    "small": {"title": 24, "subtitle": 18, "text": 12, "button": 14, "label": 12},
    "medium": {"title": 28, "subtitle": 20, "text": 14, "button": 16, "label": 14},
    "large": {"title": 32, "subtitle": 24, "text": 18, "button": 20, "label": 18}
}
current_size_preset = "medium"

def merge_dict(default, custom):
    """
    Recursively merge the custom dictionary into the default dictionary.
    
    Args:
        default (dict): The default configuration.
        custom (dict): Custom configuration to override defaults.
    Returns:
        dict: The merged dictionary.
    """
    for key, value in custom.items():
        if key in default and isinstance(default[key], dict) and isinstance(value, dict):
            merge_dict(default[key], value)
        else:
            default[key] = value
    return default

def load_theme(path=DEFAULT_THEME_PATH):
    """
    Load the custom theme from a JSON file and merge it with the default theme.
    Logs an error if the custom theme file cannot be loaded.
    
    Args:
        path (str): Path to the custom theme JSON file.
    """
    try:
        with open(path, "r") as f:
            custom_theme = json.load(f)
    except Exception as e:
        logging.error("Error loading custom theme: %s", e)
        custom_theme = {}
    
    # Copy current default theme and merge custom settings
    default_theme = ThemeManager.theme.copy()
    merged_theme = merge_dict(default_theme, custom_theme)
    palettes = merged_theme.get("palettes", {})
    palette_config = palettes.get(current_palette, {}).get(current_mode, {})
    merged_theme = merge_dict(merged_theme, palette_config)
    ThemeManager.theme = merged_theme

# Automatically load the theme upon import
load_theme()

def get_font(style=None, family=None, size=None, overstrike=False):
    """
    Retrieve a CTkFont object with the specified style parameters.
    
    Args:
        style (str): Font style key (e.g. "title", "button") used in the theme configuration.
        family (str): Desired font family (defaults to the current font).
        size (int): Specific font size (if not provided, default size is obtained from theme).
        overstrike (bool): Whether the font should be overstriked.
    Returns:
        CTkFont: Configured font object.
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
    """
    Returns the default background color for frame widgets.
    
    Returns:
        str: Default hexadecimal color code.
    """
    return ThemeManager.theme.get("CTk", {}).get("bg_color", "#08090D")

def get_ctkframe_top_color():
    """
    Returns the color defined for the top part of CTkFrame widgets.
    
    Returns:
        str: Hexadecimal color code.
    """
    return ThemeManager.theme.get("CTkFrame", {}).get("top_fg_color", "#08090D")

def load_icon(path, size=(30, 30), invert=False):
    """
    Loads an image from the given path, resizes it and optionally inverts the colors.
    
    Args:
        path (str): Path to the image.
        size (tuple): Desired size (width, height).
        invert (bool): If True, invert the colors (keeping alpha).
    Returns:
        Image: A PIL.Image object resized to the specified dimensions.
    """
    image = Image.open(path).convert("RGBA")
    if invert:
        r, g, b, a = image.split()
        rgb_image = Image.merge("RGB", (r, g, b))
        inverted_rgb = ImageOps.invert(rgb_image)
        image = Image.merge("RGBA", (*inverted_rgb.split(), a))
    return image.resize(size, Image.LANCZOS)

def set_mode(new_mode):
    """
    Change the current mode (dark/light) and reload the theme.
    
    Args:
        new_mode (str): "dark" or "light".
    """
    global current_mode
    if new_mode in ["dark", "light"]:
        current_mode = new_mode
        load_theme(DEFAULT_THEME_PATH)

def set_palette(new_palette):
    """
    Change the current palette and reload the theme.
    
    Args:
        new_palette (str): Name of the new palette.
    """
    global current_palette
    if new_palette in ThemeManager.theme.get("palettes", {}):
        current_palette = new_palette
        load_theme(DEFAULT_THEME_PATH)

def set_font(new_font):
    """
    Set the current font if it is available.
    
    Args:
        new_font (str): The name of the new font.
    """
    global current_font
    if new_font in available_fonts:
        current_font = new_font

def set_size_preset(new_preset):
    """
    Set the current font size preset.
    
    Args:
        new_preset (str): "small", "medium", or "large".
    """
    global current_size_preset
    if new_preset in font_size_presets:
        current_size_preset = new_preset

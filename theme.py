# theme.py

# List of available fonts (ensure these fonts are installed or use a ttf file loader)
AVAILABLE_FONTS = ["Helvetica", "Roboto", "Inter", "Poppins"]

# Default font settings
DEFAULT_FONT_FAMILY = "Helvetica"  # initial default
DEFAULT_FONT_SIZE = 12

def get_font(family=None, size=None, overstrike=False):
    """Return a CTkFont using the selected settings."""
    from customtkinter import CTkFont
    family = family or DEFAULT_FONT_FAMILY
    size = size or DEFAULT_FONT_SIZE
    return CTkFont(family=family, size=size, overstrike=overstrike)

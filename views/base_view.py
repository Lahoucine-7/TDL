"""
base_view.py

BaseView is a foundational class for all views in the application.
It centralizes theme loading, translation management, and common widget configuration.
All views should inherit from this class to ensure a consistent look and behavior.
"""

import customtkinter as ctk
import theme
from utils.translations import TranslationsManager

class BaseView(ctk.CTkFrame):
    def __init__(self, master, *args, language="fr", **kwargs):
        """
        Initialize BaseView.

        Args:
            master: Parent widget.
            language (str): Language code for translations. Defaults to "fr".
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(master, *args, **kwargs)
        
        # Load and apply the theme.
        theme.load_theme()
        
        # Initialize translation manager.
        self.translations = TranslationsManager(language=language)
        
        # Configure common appearance (e.g., default background color).
        self.configure(fg_color=theme.get_default_frame_color())
        
        # Additional common configuration.
        self.configure_components()

    def configure_components(self):
        """
        Configure additional common components or settings for all views.
        This method can be overridden or extended in child classes if needed.
        """
        # For now, no extra configuration is added.
        pass

    def refresh(self) -> None:
        """
        Method to refresh the view's content.
        Must be implemented by each subclass.
        """
        raise NotImplementedError("Each view must implement its own refresh() method.")

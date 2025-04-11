"""
settings_controller.py

SettingsController provides methods to manage user settings.
It supports creating/updating, retrieving, and deleting settings in the database.
"""

from datetime import datetime
import sqlite3
from database.database import connect_db, close_db

def get_current_timestamp() -> str:
    """
    Returns the current timestamp in ISO format.

    Returns:
        str: The current timestamp.
    """
    return datetime.now().isoformat()

class SettingsController:
    """
    Controller for managing user settings.
    """

    def execute_query(self, query: str, params: tuple = (), fetch: bool = False):
        """
        Executes an SQL query with the provided parameters.

        Args:
            query (str): The SQL query string.
            params (tuple): Parameters for the query.
            fetch (bool): If True, fetches the result rows.
            
        Returns:
            tuple: (rows, last_id) where rows is the fetched data (if any)
                   and last_id is the last inserted row ID.
        """
        db = None
        try:
            db = connect_db()
            if not db:
                return (None, None)
            cursor = db.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall() if fetch else None
            db.commit()
            return (rows, cursor.lastrowid)
        except sqlite3.Error as e:
            print(f"[SettingsController] Error executing query: {e}")
            return (None, None)
        finally:
            close_db(db)

    def set_setting(self, user_id: int, key: str, value: str) -> bool:
        """
        Creates or updates a setting value for a given user.
        If the key exists for the user, it updates the setting; otherwise, it creates a new entry.

        Args:
            user_id (int): The user's ID.
            key (str): The setting key (e.g., "language", "notifications").
            value (str): The value to store.
            
        Returns:
            bool: True if operation succeeded, False otherwise.
        """
        timestamp = get_current_timestamp()
        # Check if setting exists.
        query_check = "SELECT id FROM settings WHERE user_id = ? AND key = ?"
        rows, _ = self.execute_query(query_check, (user_id, key), fetch=True)
        if rows:
            # Update existing setting.
            setting_id = rows[0][0]
            query_update = "UPDATE settings SET value = ?, updated_at = ? WHERE id = ?"
            self.execute_query(query_update, (value, timestamp, setting_id))
        else:
            # Create a new setting.
            query_insert = "INSERT INTO settings (user_id, key, value, created_at, updated_at) VALUES (?, ?, ?, ?, ?)"
            _, last_id = self.execute_query(query_insert, (user_id, key, value, timestamp, timestamp))
            if last_id is None:
                return False
        return True

    def get_setting(self, user_id: int, key: str):
        """
        Retrieves the setting value for a user.

        Args:
            user_id (int): The user's ID.
            key (str): The setting key to look up.
            
        Returns:
            str or None: The setting value if found, else None.
        """
        query = "SELECT value FROM settings WHERE user_id = ? AND key = ?"
        rows, _ = self.execute_query(query, (user_id, key), fetch=True)
        if rows:
            return rows[0][0]
        return None

    def delete_setting(self, user_id: int, key: str):
        """
        Deletes a specific setting for a user.

        Args:
            user_id (int): The user's ID.
            key (str): The setting key to delete.
        """
        query = "DELETE FROM settings WHERE user_id = ? AND key = ?"
        self.execute_query(query, (user_id, key))

"""
user_controller.py

UserController manages operations related to users such as creation, update,
retrieval, deletion, and login time updates. It uses a helper function to get the current
timestamp and executes SQL queries with appropriate error handling.
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

class UserController:
    """
    Controller for managing user-related operations.
    """

    def execute_query(self, query: str, params: tuple = (), fetch: bool = False):
        """
        Executes a SQL query for user operations.

        Args:
            query (str): The SQL query string.
            params (tuple): Parameters for the SQL query.
            fetch (bool): If True, fetches and returns query results.

        Returns:
            tuple: (rows, last_id) where rows is the fetched data (if any),
                   and last_id is the last inserted row id.
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
            print(f"[UserController] Error executing query: {e}")
            return (None, None)
        finally:
            close_db(db)

    def create_user(self, username: str, email: str, password: str, theme: str = "dark") -> bool:
        """
        Creates a new user in the database.
        It is recommended to store a hashed password.

        Args:
            username (str): The user's chosen username.
            email (str): The user's unique email address.
            password (str): The user's password (preferably hashed).
            theme (str): The default theme for the user.

        Returns:
            bool: True if the user was created successfully, False otherwise.
        """
        if not username.strip():
            return False
        timestamp = get_current_timestamp()
        query = """
            INSERT INTO users (username, email, password, theme, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        _, last_id = self.execute_query(query, (username, email, password, theme, timestamp, timestamp))
        return last_id is not None

    def update_user(self, user):
        """
        Updates an existing user's information.

        Args:
            user (object): A user object with attributes including id, username, email, password, and theme.
        """
        timestamp = get_current_timestamp()
        query = """
            UPDATE users 
               SET username = ?, email = ?, password = ?, theme = ?, updated_at = ?
             WHERE id = ?
        """
        self.execute_query(query, (user.username, user.email, user.password, user.theme, timestamp, user.id))

    def get_user(self, user_id: int):
        """
        Retrieves a user's information by ID.

        Args:
            user_id (int): The user's unique identifier.

        Returns:
            dict or None: A dictionary containing user information if found, otherwise None.
        """
        query = "SELECT id, username, email, password, theme, created_at, updated_at, last_login FROM users WHERE id = ?"
        rows, _ = self.execute_query(query, (user_id,), fetch=True)
        if rows:
            row = rows[0]
            keys = ["id", "username", "email", "password", "theme", "created_at", "updated_at", "last_login"]
            return dict(zip(keys, row))
        return None

    def delete_user(self, user_id: int):
        """
        Deletes a user from the database.

        Args:
            user_id (int): The unique identifier of the user to delete.
        """
        query = "DELETE FROM users WHERE id = ?"
        self.execute_query(query, (user_id,))

    def update_last_login(self, user_id: int):
        """
        Updates the last login timestamp of a user.

        Args:
            user_id (int): The user's unique identifier.
        """
        timestamp = get_current_timestamp()
        query = "UPDATE users SET last_login = ?, updated_at = ? WHERE id = ?"
        self.execute_query(query, (timestamp, timestamp, user_id))

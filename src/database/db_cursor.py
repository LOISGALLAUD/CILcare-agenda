"""
db_cursor.py

This module contains the DBCursor class.
It will be used to interact with the database.
"""

#------------------------------------------------------------------------------#

import sqlite3 as sql

#------------------------------------------------------------------------------#

class DBCursor:
    """
    DBCursor class.

    It will be used to interact with the database.
    It will be able to return information or modify
    values in the database.
    """
    def __init__(self, app) -> None:
        self.loggers = app.loggers
        self.connection = None
        self.cursor = None
        self.setup_connection()
        self.setup_tables()
        self.setup_admin()

    def setup_connection(self) -> bool:
        """
        Connects to the database.
        """
        self.connection = sql.connect("./data/cilcare.sqlite")
        self.cursor = self.connection.cursor()
        return True

    def setup_tables(self) -> bool:
        """
        Creates the tables if they don't exist.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS `users` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `username` TEXT NOT NULL UNIQUE,
                `password` TEXT NOT NULL,
                `qualification_id` INTEGER,
                FOREIGN KEY (`qualification_id`) REFERENCES `qualifications` (`id`)
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS `qualifications` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `qualification` TEXT NOT NULL
            );
        """)
        return True

    def setup_admin(self) -> bool:
        """
        Creates the admin user if it doesn't exist.
        """
        self.cursor.execute("""
            SELECT * FROM `users` WHERE `username` = 'admin';
        """)
        if self.cursor.fetchone() is None:
            self.cursor.execute("""
                INSERT INTO `users` (`username`, `password`, `qualification_id`)
                VALUES ('admin', 'admin', NULL);
            """)
        return True

    def get_user(self, username: str) -> tuple:
        """
        Returns the user with the given username.
        """
        self.cursor.execute("""
            SELECT * FROM `users` WHERE `username` = ?;
        """, (username,))
        return self.cursor.fetchone()

    def close_connection(self) -> bool:
        """
        Ferme la session MySQL.
        """
        self.connection.close()
        return True

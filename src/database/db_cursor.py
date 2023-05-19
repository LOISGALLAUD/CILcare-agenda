"""
db_cursor.py

This module contains the DBCursor class.
It will be used to interact with the database.
"""

#------------------------------------------------------------------------------#

import mysql.connector as mysql
from src.utils.decorators import setup_service

from src.database.logins import Logins

#------------------------------------------------------------------------------#

class DBCursor:
    """
    DBCursor class.

    It will be used to interact with the database.
    It will be able to return information or modify
    values in the database.
    """
    def __init__(self, app, logins:dict) -> None:
        self.loggers = app.loggers
        self.logins = Logins(**logins)
        self.connection = None
        self.connect()

    @setup_service
    def connect(self) -> bool:
        """
        Connects to the database.
        """
        self.loggers.log.info("Connecting to the database...")
        self.connection = mysql.connect(host=self.logins.get_host(),
                                            database=self.logins.get_database(),
                                            user=self.logins.get_user(),
                                            password=self.logins.get_password(),
                                            port=self.logins.get_port())
        self.loggers.log.info("Connected to the database.")
        return True

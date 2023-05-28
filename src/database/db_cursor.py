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
    def __init__(self, app) -> None:
        self.loggers = app.loggers
        self.connection = None
        self._logins = Logins() # gets the logins from the logins.txt file
        self.setup_connection()

    @setup_service(max_attempts=5)
    def setup_connection(self) -> bool:
        """
        Connects to the database.
        """
        self.connection = mysql.connect(host=self._logins.get_host(),
                                        database=self._logins.get_database(),
                                        user=self._logins.get_user(),
                                        password=self._logins.get_password(),
                                        port=self._logins.get_port())
        self.loggers.log.info("Connected to the database.")
        return True

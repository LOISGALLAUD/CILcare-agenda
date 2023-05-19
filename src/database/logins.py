"""
logins.py

This module contains the Logins class.
Contains the logins to connect to the database.
"""

#------------------------------------------------------------------------------#

from dataclasses import dataclass

#------------------------------------------------------------------------------#

@dataclass
class Logins:
    """
    Logins class.
    Contains the logins to connect to the database.
    """
    _host: str = "localhost"
    _database: str = "cilcare_agenda"
    _user: str = "root"
    _password: str = ""
    _port: int = 3306

    def get_host(self) -> str:
        """
        Returns the host.
        """
        return self._host

    def get_database(self) -> str:
        """
        Returns the database.
        """
        return self._database

    def get_user(self) -> str:
        """
        Returns the user.
        """
        return self._user

    def get_password(self) -> str:
        """
        Returns the password.
        """
        return self._password

    def get_port(self) -> int:
        """
        Returns the port.
        """
        return self._port

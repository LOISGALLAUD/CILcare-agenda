"""
user.py

This module contains the User class.
The user is the person who uses the application.
It can be a doctor, a secretary, or an administrator.
They have to log in to use the application.
"""

#------------------------------------------------------------------------------#

from src.database.abstract_person import AbstractPerson

#------------------------------------------------------------------------------#

class User(AbstractPerson):
    """
    Current user of the application.
    """
    def setup_attributes(self):
        """
        Setup the attributes of the user.
        """

"""
abstract_class.py

This module contains the AbstractPerson class.
"""

#------------------------------------------------------------------------------#

from dataclasses import dataclass
from abc import ABC, abstractmethod

#------------------------------------------------------------------------------#

@dataclass
class AbstractPerson(ABC):
    """
    AbstractPerson class.
    """
    first_name: str = ""
    last_name: str = ""
    age: int = 0

    @abstractmethod
    def setup_attributes(self):
        """
        Setup the information of the person.
        """

"""
patient.py

This module contains the Patient class.
"""

#------------------------------------------------------------------------------#

import random
import string
from dataclasses import dataclass, field

#------------------------------------------------------------------------------#

def generate_id():
    """
    Generate a random ID of 12 uppercase letters.
    """
    return "".join(random.choices(string.ascii_uppercase, k=12))

@dataclass(frozen=False, kw_only=False)
class Patient:
    """
    Patient class.
    """
    first_name: str
    last_name: str
    age: int
    active: bool = True
    mail: list[str] = field(default_factory=list)
    _identifier: str = field(init=False, default_factory=generate_id, repr=False)

#------------------------------------------------------------------------------#

if __name__ == "__main__":
    person = Patient("Loïs", "GALLAUD", 19,
                     mail=["loisgallaud@hotmail.com", "gallaudlois@gmail.com"])
    person1 = Patient("Pierrick","BOUILLOUX", 20,
                      mail=["pierrickb@gmail.com"])
    print(person)
    print(person1)

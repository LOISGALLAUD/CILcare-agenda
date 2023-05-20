"""
main.py

Entrypoint of the application.
It launches the application.
"""

#------------------------------------------------------------------------------#

from src.cilcare_agenda import Agenda

#------------------------------------------------------------------------------#

if __name__ == "__main__":
    print("Starting CILcare agenda...")
    agenda = Agenda()
    print("CILcare agenda stopped.")

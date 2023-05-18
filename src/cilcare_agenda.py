"""
cilcare_agenda.ŷ

Encapsulates the whole logic of the application
as well as the connections to the database.
"""

#------------------------------------------------------------------------------#

import time

from src.loggers import Loggers
from src.interface.user_interface import GUI

#------------------------------------------------------------------------------#


class Agenda:
    """
    Agenda application.
    """

    NAME = "CILcare_Agenda"
    VERSION = "0.1"
    AUTHOR = "Loïs GALLAUD"

    def __init__(self):
        """
        Agenda constructor.
        """
        self.start_time = time.time()

        # Setup the loggers
        self.loggers = Loggers(Agenda.NAME)
        self.loggers.log.info("Starting %s v%s...", Agenda.NAME, Agenda.VERSION)

        # Setup the current user

        # Setup the database connection

        # Setup the GUI
        self.gui = GUI(self)

        self.gui.start()

    def close(self):
        """
        Quits the application.
        """
        # Close the database connection safely
        # self.database.close()
        # Close the rest of the application
        self.gui.close()
        self.loggers.log.info("Closing %s...", Agenda.NAME)
        self.loggers.close()

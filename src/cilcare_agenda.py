"""
cilcare_agenda.

Encapsulates the whole logic of the application
as well as the connections to the database.
"""

#------------------------------------------------------------------------------#

import time
from src.utils.loggers import Loggers
from src.database.db_cursor import DBCursor
from src.interface.user_interface import GUI

#------------------------------------------------------------------------------#


class Agenda:
    """
    Agenda application.
    """

    NAME = "CILpink_Agenda"
    VERSION = "0.1"
    AUTHOR = "Loïs GALLAUD"

    def __init__(self) -> None:
        """
        Agenda constructor.
        """
        self.start_time = time.time()

        # Setup the loggers
        self.loggers = Loggers(Agenda.NAME)
        self.loggers.log.debug( "Starting %s v%s...", Agenda.NAME, Agenda.VERSION)

        # Setup the current user
        self.current_user = None

        # Setup the database connection
        self.loggers.log.info("Connecting to the database...")
        self.db_cursor = DBCursor(self)
        self.loggers.log.info("Connected to the database.")

        # Setup the GUI
        self.gui = GUI(self)
        self.gui.protocol("WM_DELETE_WINDOW", self.close)

        self.gui.start()

    def close(self) -> bool:
        """
        Quits the application.
        """
        # Close the database connection safely
        self.db_cursor.close_connection()
        self.loggers.log.info("Disconnected from the database.")
        # Close the rest of the application
        self.gui.close()
        self.loggers.log.info("Closing %s...", Agenda.NAME)
        self.loggers.close()
        return True

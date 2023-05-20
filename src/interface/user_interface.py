"""
user_interface.py

This module defines the GUI class
to manage the graphical user interface
of the application.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Tk

#-------------------------------------------------------------------#

class GUI(Tk):
    """
    Graphical User Interface of the application.
    """
    def __init__(self, app) -> None:
        super().__init__()
        self.app = app
        self.loggers = app.loggers
        self.title = app.NAME
        self.geometry("800x480")
        self.resizable = False
        self.config(bg="black")

    def start(self) -> bool:
        """
        Displays the GUI.
        """
        self.loggers.log.info("GUI started")
        self.mainloop()
        return True

    def close(self) -> bool:
        """
        Closes the GUI.
        """
        self.quit()
        self.loggers.log.info("GUI closed.")
        return True

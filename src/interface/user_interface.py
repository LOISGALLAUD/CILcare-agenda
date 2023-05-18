"""
user_interface.py

This module defines the GUI class
to manage the graphical user interface
of the application.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Tk
from src.utils.decorators import setup_service

#-------------------------------------------------------------------#

class GUI(Tk):
    """
    Graphical User Interface of the application.
    """
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.loggers = app.loggers

        self.setup_window()

    @setup_service
    def setup_window(self) -> bool:
        """
        Setup the window of the application.
        Returns True if the window was successfully setup.
        """
        self.title(self.app.NAME)
        self.geometry("800x480")
        self.resizable(False, False)
        #self.iconbitmap(os.path.join(os.getcwd(),"DATA","IMAGES","logo.ico"))
        self.protocol("WM_DELETE_WINDOW", self.app.close)
        self.config(bg="black")
        return True

    def start(self) -> None:
        """
        Displays the GUI.
        """
        self.loggers.log.info("GUI started")
        self.mainloop()

    def close(self) -> bool:
        """
        Closes the GUI.
        """
        self.loggers.log.info("GUI closed")
        self.quit()
        return True

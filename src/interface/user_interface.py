"""
user_interface.py

This module defines the GUI class
to manage the graphical user interface
of the application.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Tk, Frame, BOTH
from src.interface.menus.login_menu import LoginMenu
from src.interface.menus.main_menu import MainMenu
from src.interface.menus.help_menu import HelpMenu

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

        self.login_menu = None
        self.current_menu = None

        self.setup_menus()

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

    def setup_menus(self):
        """
        Setup the different menus of the application.
        """
        self.login_menu = LoginMenu(self)
        self.help_menu = HelpMenu(self)
        #self.settings_menu = SettingsMenu(self)
        self.main_menu = MainMenu(self)

        #self.shopping_menu = ShoppingMenu(self)
        #self.history_menu = Frame(self)
        #self.stats_menu = Frame(self)

        self.main_menu.pack(fill=BOTH, expand=True)
        self.current_menu = self.main_menu

    def change_menu(self, next_menu: Frame):
        """
        This function changes the current view to the desired menu.
        """
        # Don't do anything if the desired menu is the same as the current menu
        if next_menu == self.current_menu:
            return

        # Unbind the keyboard
        self.unbind("<Key>")

        self.current_menu.pack_forget()
        next_menu.pack(fill=BOTH, expand=True)
        # Update the current menu reference
        self.current_menu = next_menu
        self.loggers.log.debug(f"({type(next_menu).__name__})")

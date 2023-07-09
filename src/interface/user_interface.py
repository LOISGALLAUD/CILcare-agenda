"""
user_interface.py

This module defines the GUI class
to manage the graphical user interface
of the application.
"""

#-------------------------------------------------------------------#

import os
from PIL import Image, ImageTk
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
        self.title(app.NAME)
        self.attributes("-fullscreen", True)
        self.resizable = False
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.coeffx = self.winfo_screenheight() // 1080
        self.coeffy = self.winfo_screenwidth() // 1920

        self.cilcare_logo = None
        self.login_menu = None
        self.current_menu = None

        self.load_images()
        self.setup_menus()

        # Set the GUI reference in the application
        setattr(self.app, "gui", self)
        self.mainloop()

    def close(self) -> bool:
        """
        Closes the GUI.
        """
        self.quit()
        self.loggers.log.info("GUI closed.")
        return True

    def setup_menus(self) -> bool:
        """
        Setup the different menus of the application.
        """
        self.login_menu = LoginMenu(self)
        self.main_menu = MainMenu(self)
        self.help_menu = HelpMenu(self)

        self.current_menu = self.main_menu
        return True

    def change_menu(self, next_menu: Frame) -> bool:
        """
        This function changes the current view to the desired menu.
        """
        # Don't do anything if the desired menu is the same as the current menu
        if next_menu == self.current_menu:
            return
        self.current_menu.pack_forget()
        next_menu.pack(fill=BOTH, expand=True)

        # Update the current menu reference
        self.current_menu = next_menu
        self.loggers.log.debug(f"({type(next_menu).__name__})")
        return True

    def load_images(self) -> None:
        """
        Load every image of the application.
        """
        self.cilcare_logo = self.open_image("cilcare_logo.png", 100, 100)

    def open_image(self, file_name: str,
                    width:int=None, height:int=None) -> ImageTk.PhotoImage:
        """
        This function loads an image from the given path.
        """
        image_path = os.path.join(os.getcwd(), "data", "images", file_name)
        image = Image.open(image_path)
        if width and height:
            image = image.resize((width*self.coeffx, height*self.coeffy), Image.ANTIALIAS)

        photo = ImageTk.PhotoImage(image)
        return photo

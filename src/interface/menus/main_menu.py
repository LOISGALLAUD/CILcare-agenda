"""
main_menu.py

Configure the main menu of the application.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame
from src.interface.menus.left.left_grid import LeftGrid
from src.interface.menus.right.right_grid import RightGrid

#-------------------------------------------------------------------#

class MainMenu(Frame):
    """
    Agenda's main page.

    It is the first page to appear when the user logs in.
    """
    def __init__(self, gui=None) -> None:
        super().__init__(gui)
        self.gui = gui

        # Setup the left grid for the navbar
        self.left_grid = LeftGrid(self)
        self.left_grid.grid(row=0, column=0, sticky='nsew')

        # Setup the right grid for the header, body and footer
        self.right_grid = RightGrid(self)
        self.right_grid.grid(row=0, column=1, sticky='nsew')

        # Setup the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)


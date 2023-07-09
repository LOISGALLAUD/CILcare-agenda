"""
LeftGrid.py

Container of the navbar of the shopping page.
"""

#-------------------------------------------------------------------#

from src.interface.menus.left.navbar import Navbar
from src.utils.graphical_utils import Frame

#-------------------------------------------------------------------#


class LeftGrid(Frame):
    """
    Container of the navbar of the shopping page.
    """
    def __init__(self, main_menu=None):
        super().__init__(main_menu)
        self.manager = main_menu
        self.grid(row=0, column=0, sticky='nsew')
        self.update_idletasks()

        self.grid_propagate(False)

        self.navbar = Navbar(self)
        self.navbar.pack(fill='both', expand=True, side='left')

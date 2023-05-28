"""
LeftGrid.py

Container of the navbar of the shopping page.
"""

#-------------------------------------------------------------------#

from src.interface.menus.left.navbar import Navbar
from src.utils.graphical_utils import Frame, ButtonApp

#-------------------------------------------------------------------#


class LeftGrid(Frame):
    """
    Container of the navbar of the shopping page.
    """
    def __init__(self, main_menu=None):
        super().__init__(main_menu)
        self.manager = main_menu

        self.grid_propagate(False)

        self.navbar = Navbar(self)
        self.compact_btn = ButtonApp(self, text="<<",
                                         command=self.compact_navbar)

        self.navbar.pack(fill='both', expand=True, side='left')
        self.compact_btn.pack(fill='both', side='right')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

    def compact_navbar(self) -> None:
        """
        Compacts the navbar to the left of the screen.
        """
        self.navbar.pack_forget()
        self.compact_btn.config(text=">>", command=self.expand_navbar)

        # Responsive
        self.manager.grid_columnconfigure(0, weight=0)
        self.manager.grid_columnconfigure(1, weight=1)

    def expand_navbar(self) -> None:
        """
        Expands the navbar to the left of the screen.
        """
        self.navbar.pack(fill='both', expand=True, side='left')
        self.compact_btn.config(text="<<", command=self.compact_navbar)

        # Responsive
        self.manager.grid_columnconfigure(0, weight=1)
        self.manager.grid_columnconfigure(1, weight=6)

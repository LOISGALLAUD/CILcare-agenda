"""
header.py

Top section of the shopping menu.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame

#-------------------------------------------------------------------#


class Header(Frame):
    """
    Top section of the shopping menu.
    """
    def __init__(self, manager=None) -> None:
        super().__init__(manager)
        self.manager = manager

        self.grid_propagate(False)
        self.configure(bg="#2bb5a6")


"""
right_click.py

This file contain the menu object displayed
next to the mouse when right clicking.
"""

#------------------------------------------------------------------------------#

from src.utils.graphical_utils import Menu

#------------------------------------------------------------------------------#

class RightClickMenu(Menu):
    """
    Frame displaying when right clicking.
    """
    def __init__(self, manager):
        super().__init__(manager)
        self.config(tearoff=False)
        self.add_command(label="Option 1", command=lambda: print("Option 1 selected"))
        self.add_command(label="Option 2", command=lambda: print("Option 2 selected"))
        self.add_separator()
        self.add_command(label="Quitter", command=None)

    def show(self, event):
        """
        Shows the menu at the given coordinates.
        """
        self.tk_popup(event.x_root, event.y_root)

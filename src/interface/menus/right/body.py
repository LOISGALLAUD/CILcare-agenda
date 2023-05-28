"""
body.py

Configure MarcoNeo's body on its shopping menu.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame

#-------------------------------------------------------------------#

class Body(Frame):
    """
    Contains the items to be displayed in the shopping page.
    """
    def __init__(self, manager=None):
        super().__init__(manager)
        self.manager = manager
        self.grid_propagate(False)
        self.configure(bg="#EEEEEE")

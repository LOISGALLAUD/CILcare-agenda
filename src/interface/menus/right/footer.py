"""
footer.py

Describes the footer of the shopping menu.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame

#-------------------------------------------------------------------#

class Footer(Frame):
    """
    Footer of the shopping menu.
    Contains the confirm button and the reset button
    and the total of the cart.
    """
    def __init__(self, manager=None):
        super().__init__(manager)
        self.shopping_manager = manager.manager
        self.loggers = self.shopping_manager.gui.app.loggers
        self.grid_propagate(False)
        self.configure(bg="#2bb5a6")

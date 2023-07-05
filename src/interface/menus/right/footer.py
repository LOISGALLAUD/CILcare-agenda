"""
footer.py

Describes the footer of the shopping menu.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame
from src.interface.widgets.schedule_picker import SchedulePicker

#-------------------------------------------------------------------#

class Footer(Frame):
    """
    Footer of the shopping menu.
    Contains the confirm button and the reset button
    and the total of the cart.
    """
    def __init__(self, manager=None):
        super().__init__(manager)
        self.grid(row=2, column=0, sticky='nsew')
        self.update_idletasks()
        self.shopping_manager = manager.manager
        self.loggers = self.shopping_manager.gui.app.loggers
        self.grid_propagate(False)
        self.configure(bg="#8c77ff")

        SchedulePicker(self).pack(side="left", padx=10, pady=10)

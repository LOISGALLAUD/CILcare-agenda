"""
right_grid.py

Container of the header, body and footer of the shopping page.
"""

#-------------------------------------------------------------------#

from src.interface.menus.right.header import Header
from src.interface.menus.right.body import Body
from src.interface.menus.right.footer import Footer
from src.utils.graphical_utils import Frame

#-------------------------------------------------------------------#


class RightGrid(Frame):
    """
    Container of the header, body and footer of the shopping page.
    """
    def __init__(self, main_menu=None):
        super().__init__(main_menu, bg='white')
        self.manager = main_menu
        self.grid_propagate(False)
        self.grid(row=0, column=1, sticky='nsew')
        self.update_idletasks()

        # Setup the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=12)
        self.grid_rowconfigure(2, weight=1)

        # Setup the header inside the right grid
        self.header = Header(self)

        # Setup the footer inside the right grid
        self.footer = Footer(self)

        # Setup the body inside the right grid
        self.body = Body(self)


    def reset_modifications(self) -> None:
        """
        Resets the modifications made by the user.
        """
        self.header.reset_modifications()
        #self.body.reset_modifications()
        #self.footer.reset_modifications()

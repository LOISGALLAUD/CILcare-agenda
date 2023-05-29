"""
body.py

Configure MarcoNeo's body on its shopping menu.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Canvas

#-------------------------------------------------------------------#

class Body(Canvas):
    """
    Contains the items to be displayed in the shopping page.
    """
    def __init__(self, right_grid=None):
        super().__init__(right_grid)
        self.manager = right_grid
        self.configure(bg="#FFFFFF")
        self.width = None
        self.height = None

        # Responsive design
        self.bind("<Configure>", self.draw_timeline)

    def draw_timeline(self, _event=None):
        """
        Draw a line from left to right.
        """
        self.manager.manager.gui.update()
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.create_line(0, self.height//5,
                         self.width, self.height//5,
                         fill="#A91B60", width=5)

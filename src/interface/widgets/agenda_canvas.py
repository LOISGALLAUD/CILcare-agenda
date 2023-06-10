"""
agenda_canvas.py

Describe the agenda canvas in the add days off menu.
It contains visual representation of the disponibilities
of operators.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Canvas

#-------------------------------------------------------------------#

class AgendaCanvas(Canvas):
    """
    Describe the agenda canvas in the add days off menu.
    It contains visual representation of the disponibilities
    of operators.
    """
    def __init__(self, manager=None, **kwargs) -> None:
        super().__init__(manager, **kwargs)
        self.manager = manager
        self.width = None
        self.height = None
        self.setup_canvas()

    def setup_canvas(self) -> None:
        """
        Setup the canvas.
        """
        self.configure(bg="#2bb5a6")
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event) -> None:
        """
        Resize the canvas.
        """
        self.width = event.width
        self.height = event.height
        self.configure(width=self.width, height=self.height)
        self.delete("all")
        self.draw_grid()

    def draw_grid(self) -> None:
        """
        Draw the grid on the canvas.
        """
        # Draw the horizontal lines
        for i in range(24):
            self.create_line(0, i * self.height / 24, self.width,
                             i * self.height / 24, fill="#3f3f3f")

        # Draw the vertical lines
        for i in range(7):
            self.create_line(i * self.width / 7, 0, i * self.width / 7,
                             self.height, fill="#3f3f3f")

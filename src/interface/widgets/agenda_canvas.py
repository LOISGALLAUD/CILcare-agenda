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
    Represents the agenda canvas.
    """
    def __init__(self, master, start_time, end_time, **kwargs):
        super().__init__(master, width=master.winfo_reqwidth(),
                         height=master.winfo_reqheight(), **kwargs)
        self.master = master
        self.start_time = start_time
        self.end_time = end_time
        self.step = self.winfo_width() / 24  # 1 hour
        self.create_timeline()
        self.selected_rectangles = []  # Liste des rectangles sélectionnés
        self.bind('<Button-1>', self.deselect_rectangles)

    def deselect_rectangles(self, _event) -> None:
        """
        Deselect all rectangles when clicking on the canvas.
        """
        item = self.find_withtag('current')  # Récupérer l'élément sur lequel le clic a eu lieu
        if len(item) == 1 and self.type(item) == 'rectangle':
            return  # Ne rien faire si le clic a eu lieu sur un rectangle
        if len(item) == 1 and self.type(item) == 'text':
            return # Ne rien faire si le clic a eu lieu sur un texte

        for rect in self.selected_rectangles:
            self.itemconfig(rect.rect, fill='darkred')
        self.selected_rectangles.clear()

    def create_timeline(self):
        """
        Creates the timeline.
        """
        timeline_width = self.master.winfo_reqwidth()
        timeline_height = self.master.winfo_reqheight()

        # Steps
        step_width = timeline_width / 24

        # Draw the timeline
        for i in range(25):  # Increase to 25 to draw line at the end
            x_pos = i * step_width
            self.create_line(x_pos, 0, x_pos, timeline_height, fill='black')
            time_label = self.start_time + i
            self.create_text(x_pos+step_width/5, 5*timeline_height/6,
                             text=str(time_label), anchor='n', fill='black')

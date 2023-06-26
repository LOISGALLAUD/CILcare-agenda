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
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="white", **kwargs)
        self.master = master
        self.width = 0
        self.height = 0
        self.pack(fill='both', expand=True)
        self.update_idletasks()

        self.time_interval = 24  # 24 hours
        self.time_step = 1 # 1 hour
        self.x_step = self.width / self.time_interval
        self.start_time = 0
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
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.x_step = self.width / self.time_interval
        timeline_height = self.height

        # Draw the timeline
        for i in range(self.time_interval):  # Increase to 25 to draw line at the end
            x_pos = i * self.x_step
            self.create_line(x_pos, 0, x_pos, timeline_height, fill='#d9d9d9')
            time_label = self.start_time + i
            self.create_text(x_pos+self.x_step/5, 11*timeline_height/12,
                             text=str(time_label), anchor='n', fill='grey')

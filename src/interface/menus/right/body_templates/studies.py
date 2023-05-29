"""
studies.py

Studies template for the body
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, Canvas

#-------------------------------------------------------------------#

class StudiesTemplate(Frame):
    """
    Contains the Frame in which will be displayed every
    templates related to the studies.
    """
    def __init__(self, body=None):
        super().__init__(body)
        self.manager = body
        self.configure(bg="#FFFFFF")
        self.width = None
        self.height = None
        self.days_off_timeline = None
        self.study_timeline = None
        self.setup_studies()
        self.setup_off_days_timeline()

    def setup_off_days_timeline(self) -> None:
        """
        Setup the template of days off.
        """
        self.days_off_timeline = DaysOffTimelineTemplate(self)
        self.days_off_timeline.pack(fill='both', expand=True, side='top', padx=10, pady=10)

    def setup_studies(self) -> None:
        """
        Setup the template of studies.
        """
        self.study_timeline = StudyTimelineTemplate(self)
        self.study_timeline.pack(fill='both', expand=True, side='top', padx=10, pady=10)

#-------------------------------------------------------------------#

class DaysOffTimelineTemplate(Canvas):
    """
    Contains the timeline of the days off.
    """
    def __init__(self, body=None):
        super().__init__(body)
        self.manager = body
        self.configure(bg="red")
        self.width = None
        self.height = None

        # Responsive design
        self.bind("<Configure>", self.draw_timeline)

    def draw_timeline(self, _event=None) -> None:
        """
        Draw a line from left to right.
        """
        self.manager.manager.manager.manager.gui.update()
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.create_line(0, self.height//5,
                         self.width, self.height//5,
                         fill="#000000", width=5)

#-------------------------------------------------------------------#

class StudyTimelineTemplate(Canvas):
    """
    Contains the timeline of the days off.
    """
    def __init__(self, body=None):
        super().__init__(body)
        self.manager = body
        self.configure(bg="blue")
        self.width = None
        self.height = None

        # Responsive design
        self.bind("<Configure>", self.draw_timeline)

    def draw_timeline(self, _event=None) -> None:
        """
        Draw a line from left to right.
        """
        self.manager.manager.manager.manager.gui.update()
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.create_line(0, self.height//5,
                         self.width, self.height//5,
                         fill="#000000", width=5)

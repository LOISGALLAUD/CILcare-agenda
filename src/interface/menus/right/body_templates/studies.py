"""
studies.py

Studies template for the body
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, Canvas, Label

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
        self.setup_off_days_timeline()
        self.setup_studies()

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

class DaysOffTimelineTemplate(Frame):
    """
    Contains the timeline of the days off.
    """
    def __init__(self, body=None):
        super().__init__(body)
        self.manager = body
        self.configure(bg="red")
        self.timeline_width = None
        self.timeline_height = None
        self.timeline = None

        self.setup_labels()
        self.setup_timeline_canvas()

    def setup_labels(self) -> None:
        """
        Setup the labels of the timeline.
        """
        Label(self, text="Days off / Availabilities", bg="#FFFFFF",
              fg="#000000", font=("System", 12)).pack(fill='both',
                                                      side='left', padx=10, pady=10)

    def setup_timeline_canvas(self) -> None:
        """
        Setup the canvas of the timeline.
        """
        self.timeline = Canvas(self, bg="#FFFFFF")
        self.timeline.pack(fill='both', expand=True, side='left', padx=10, pady=10)

        # Responsive design
        self.timeline.bind("<Configure>", self.draw_timeline)

    def draw_timeline(self, _event=None) -> None:
        """
        Draw a line from left to right.
        """
        self.manager.manager.manager.manager.gui.update()
        self.timeline_width = self.timeline.winfo_width()
        self.timeline_height = self.timeline.winfo_height()
        self.timeline.create_line(0, self.timeline_height//5,
                         self.timeline_width, self.timeline_height//5,
                         fill="#000000", width=5)

#-------------------------------------------------------------------#

class StudyTimelineTemplate(Frame):
    """
    Contains the timeline of the days off.
    """
    def __init__(self, body=None):
        super().__init__(body)
        self.manager = body
        self.configure(bg="blue")
        self.timeline_width = None
        self.timeline_height = None
        self.timeline = None

        self.setup_labels()
        self.setup_timeline_canvas()

    def setup_labels(self) -> None:
        """
        Setup the labels of the timeline.
        """
        Label(self, text="Study", bg="#FFFFFF",
              fg="#000000", font=("System", 12)).pack(fill='both',
                                                      side='left', padx=10, pady=10)
        frame = Frame(self, bg="#FFFFFF")
        Label(frame, text="Serial1", bg="#FFFFFF").pack(fill='both', side='top', padx=10, pady=10)
        Label(frame, text="Serial2", bg="#FFFFFF").pack(fill='both', side='top', padx=10, pady=10)
        frame.pack(fill='both', side='left', padx=10, pady=10)

    def setup_timeline_canvas(self) -> None:
        """
        Setup the canvas of the timeline.
        """
        self.timeline = Canvas(self, bg="#FFFFFF")
        self.timeline.pack(fill='both', expand=True, side='left', padx=10, pady=10)

        # Responsive design
        self.timeline.bind("<Configure>", self.draw_timeline)

    def draw_timeline(self, _event=None) -> None:
        """
        Draw a line from left to right.
        """
        self.manager.manager.manager.manager.gui.update()
        self.timeline_width = self.timeline.winfo_width()
        self.timeline_height = self.timeline.winfo_height()
        self.timeline.create_line(0, self.timeline_height//5,
                         self.timeline_width, self.timeline_height//5,
                         fill="#000000", width=5)

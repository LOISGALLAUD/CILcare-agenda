"""
studies.py

Studies template for the body
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, Canvas, Label, ButtonApp, LabelEntryPair

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
        self.days_off_frame = None
        self.study_frame = None
        self.add_study = None

        # By default, the body contains the days off timeline and the study timeline
        self.setup_off_days_frame()
        self.setup_studies_frame()

    def setup_off_days_frame(self) -> None:
        """
        Setup the template of days off.
        """
        self.days_off_frame = DaysOffTimelineTemplate(self)
        self.days_off_frame.pack(fill='both', expand=True, side='top', padx=10, pady=10)

    def setup_studies_frame(self) -> None:
        """
        Setup the template of studies.
        """
        self.study_frame = StudyTimelineTemplate(self)
        self.study_frame.pack(fill='both', expand=True, side='top', padx=10, pady=10)

    def back_to_studies_frame(self) -> None:
        """
        Back to the studies frame.
        """
        self.add_study.pack_forget()
        self.setup_studies_frame()
        self.setup_off_days_frame()

    def setup_add_study(self) -> None:
        """
        Setup the template of adding a study.
        """
        self.study_frame.pack_forget()
        self.days_off_frame.pack_forget()
        self.add_study = AddStudyTemplate(self)
        self.add_study.pack(fill='both', expand=True, side='top', padx=10, pady=10)

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

#-------------------------------------------------------------------#

class AddStudyTemplate(Frame):
    """
    Templates displayed when the user wants to add a study.
    """
    parameters = ["Study name", "Client name", "Animal type", "Number", "Description"]
    def __init__(self, study_template) -> None:
        super().__init__(study_template)
        self.manager = study_template
        self.configure(bg="#FFFFFF")

        # Parameters of the study
        for parameter in self.parameters:
            LabelEntryPair(self, parameter).pack(fill='both', side='top', padx=10)
        # Serials of the study

        #---------<Serials>-------------------------------------------#

        # Back button
        self.back_btn = ButtonApp(self, text="Back", bg="#FFFFFF",
                                  fg="#000000", command=self.manager.back_to_studies_frame)
        self.back_btn.pack(fill='both', side='top', padx=10, pady=10)


class Serials:
    """
    Unsorted serials of the study.
    The user can add as many serials as he wants.
    Scrollable frame.
    """

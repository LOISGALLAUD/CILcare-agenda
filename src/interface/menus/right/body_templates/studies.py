"""
studies.py

Studies template for the body
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, Canvas, Label, ButtonApp, Entry
from src.utils.graphical_utils import LabelEntryPair, Serials, IntVar, Checkbutton
from src.interface.widgets.right_click import RCMSerial, RCMStudy

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
        self.days_off_frame.pack(fill='both', expand=True, side='top')

    def setup_studies_frame(self) -> None:
        """
        Setup the template of studies.
        """
        self.study_frame = StudyTimelineTemplate(self)
        self.study_frame.pack(fill='both', expand=True, side='top')

    def back_to_studies_frame(self) -> None:
        """
        Back to the studies frame.
        """
        self.manager.manager.header.reset_modifications()
        self.add_study.pack_forget()
        self.add_study = None
        self.setup_studies_frame()
        self.setup_off_days_frame()

    def setup_add_study(self) -> None:
        """
        Setup the template of adding a study.
        """
        if self.add_study is not None:
            return
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
        self.timeline_width = None
        self.timeline_height = None
        self.timeline = None
        self.right_click_menu_study = RCMStudy(self)

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

        # Bind the right click menu to the canvas
        self.timeline.bind("<Button-3>", self.right_click_menu_study.show)

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
        self.timeline_width = None
        self.timeline_height = None
        self.timeline = None
        self.right_click_menu_study = RCMStudy(self)
        self.right_click_menu_serial = RCMSerial(self)

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
        frame.bind("<Button-3>", self.right_click_menu_serial.show)

        Label(frame, text="Serial1", bg="#FFFFFF").pack(fill='both', side='top', padx=10, pady=10)
        Label(frame, text="Serial2", bg="#FFFFFF").pack(fill='both', side='top', padx=10, pady=10)
        frame.pack(fill='both', side='left', padx=10, pady=10)

    def setup_timeline_canvas(self) -> None:
        """
        Setup the canvas of the timeline.
        """
        self.timeline = Canvas(self, bg="#FFFFFF")
        self.timeline.pack(fill='both', expand=True, side='left', padx=10, pady=10)

        # Bind the right click menu to the canvas
        self.timeline.bind("<Button-3>", self.right_click_menu_study.show)

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
    parameters = ["Study name", "Client name", "Animal type", "Number"]
    def __init__(self, study_template) -> None:
        super().__init__(study_template)
        self.manager = study_template
        self.configure(bg="#FFFFFF")

        self.checkbox_var = IntVar()

        # Parameters of the study
        for parameter in self.parameters:
            LabelEntryPair(self, parameter).pack(fill='both', side='top', padx=10)

        self.checkbox = Checkbutton(self, text="Archived", bg="#FFFFFF", activebackground="#FFFFFF",
                               variable=self.checkbox_var, command=None)
        self.checkbox.pack(side='top', padx=10, pady=10, anchor="w")

        # Description of the study
        self.description = Entry(self, text="Description")
        self.description.bind('<Return>', self.line_break)
        self.description.pack(fill='both', side='top', padx=10)

        # Serials of the study
        self.serials = Serials(self)
        self.serials.pack(fill='both', side='top', padx=10, pady=10)

        # Bottom widget
        self.bottom_frame = Frame(self, bg="white")
        self.bottom_frame.pack(fill='both', side='bottom', padx=10, pady=10)
        self.confirm_btn = ButtonApp(self.bottom_frame, text="Confirm",
                                     command=self.manager.back_to_studies_frame)
        self.back_btn = ButtonApp(self.bottom_frame, text="Back",
                                  command=self.manager.back_to_studies_frame)
        self.confirm_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)
        self.back_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)

    def line_break(self, _event) -> None:
        """
        Jump a line in the description entrybox.
        """
        self.description.insert('end', '\n')
        print("sexe")

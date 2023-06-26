"""
studies.py

Studies template for the body
"""

#-------------------------------------------------------------------#

from tkcolorpicker import askcolor
from src.utils.graphical_utils import Frame, Canvas, Label, ButtonApp, Text
from src.utils.graphical_utils import LabelEntryPair, Serials, IntVar, Checkbutton
from src.interface.widgets.schedule_picker import SchedulePicker
from src.interface.widgets.right_click import RCMSerial, RCMStudy
from src.interface.widgets.agenda_canvas import AgendaCanvas
from src.interface.widgets.task_rectangle import TaskRectangle

#-------------------------------------------------------------------#

class StudiesTemplate(Frame):
    """
    Contains the Frame in which will be displayed every
    templates related to the studies.
    """
    def __init__(self, body=None):
        super().__init__(body, bg="#FFFFFF")
        self.manager = body
        self.pack(fill='both', expand=True, side='top')
        self.update_idletasks()

        self.days_off_frame = None
        self.study_frame = None
        self.add_study = None
        self.add_days_off = None

        # By default, the body contains the days off timeline and the study timeline
        self.setup_off_days_frame()
        self.setup_studies_frame()
        self.days_off_frame.agenda_canvas.create_timeline()
        self.study_frame.agenda_canvas.create_timeline()
        self.days_off_frame.display_tasks()
        self.study_frame.display_tasks()

    def setup_off_days_frame(self) -> None:
        """
        Setup the template of days off.
        """
        self.days_off_frame = DaysOffTimelineTemplate(self)

    def setup_studies_frame(self) -> None:
        """
        Setup the template of studies.
        """
        self.study_frame = StudyTimelineTemplate(self)

    def from_addstudy_to_studies_frame(self) -> None:
        """
        Back to the studies frame.
        """
        self.manager.manager.header.reset_modifications()
        self.add_study.pack_forget()
        self.add_study = None
        self.setup_studies_frame()
        self.setup_off_days_frame()

    def from_adddaysoff_to_studies_frame(self) -> None:
        """
        Back to the studies frame.
        """
        self.manager.manager.header.reset_modifications()
        self.add_days_off.pack_forget()
        self.add_days_off = None
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

    def setup_add_days_off(self) -> None:
        """
        Setup the template of adding days off.
        """
        if self.add_days_off is not None:
            return
        self.study_frame.pack_forget()
        self.days_off_frame.pack_forget()
        self.add_days_off = AddDaysOffTemplate(self)
        self.add_days_off.pack(fill='both', expand=True, side='top', padx=10, pady=10)

#-------------------------------------------------------------------#

class DaysOffTimelineTemplate(Frame):
    """
    Contains the timeline of the days off.
    """
    def __init__(self, body=None):
        super().__init__(body)
        self.manager = body
        self.pack(fill='both', expand=True, side='top')
        self.update_idletasks()
        self.right_click_menu_study = RCMStudy(self)

        self.setup_timeline_canvas()

    def setup_timeline_canvas(self) -> None:
        """
        Setup the canvas of the timeline.
        """
        self.agenda_canvas = AgendaCanvas(self)

        # Bind the right click menu to the canvas
        self.agenda_canvas.bind("<Button-3>", self.right_click_menu_study.show)

    def display_tasks(self) -> None:
        """
        Display the tasks on the timeline.
        """
        TaskRectangle(self.agenda_canvas, "Vacances hugo", 8, 12)
        TaskRectangle(self.agenda_canvas, "Astreintes Aurore", 14, 18)
        TaskRectangle(self.agenda_canvas, "Vacances Hugo", 20, 22)


#-------------------------------------------------------------------#

class StudyTimelineTemplate(Frame):
    """
    Contains the timeline of the days off.
    """
    def __init__(self, body=None):
        super().__init__(body)
        self.manager = body
        self.pack(fill='both', expand=True, side='top')
        self.update_idletasks()

        self.right_click_menu_study = RCMStudy(self)
        self.right_click_menu_serial = RCMSerial(self)

        self.setup_timeline_canvas()

    def setup_timeline_canvas(self) -> None:
        """
        Setup the canvas of the timeline.
        """
        self.agenda_canvas = AgendaCanvas(self)
        self.agenda_canvas.pack( fill='both', expand=True)

        # Bind the right click menu to the canvas
        self.agenda_canvas.bind("<Button-3>", self.right_click_menu_study.show)

    def display_tasks(self) -> None:
        """
        Display the tasks on the timeline.
        """
        TaskRectangle(self.agenda_canvas, "TASK1", 8, 12)
        TaskRectangle(self.agenda_canvas, "TASK2", 14, 18)
        TaskRectangle(self.agenda_canvas, "TASK3", 20, 22)

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


        # Parameters of the study
        for parameter in self.parameters:
            LabelEntryPair(self, parameter).pack(fill='both', side='top', padx=10)

        self.checkbox_var = IntVar()
        self.checkbox = Checkbutton(self, text="Archived", bg="#FFFFFF", activebackground="#FFFFFF",
                               variable=self.checkbox_var, command=None)
        self.checkbox.pack(side='top', padx=10, pady=10, anchor="w")

        # Description of the study
        Label(self, text="Description", bg="#FFFFFF").pack(fill='both', side='top', padx=10)
        self.description = Text(self)
        self.description.pack(fill='both', side='top', padx=10)

        # Serials of the study
        self.serials = Serials(self)
        self.serials.pack(fill='both', side='top', padx=10, pady=10)

        # Bottom widget
        self.bottom_frame = Frame(self, bg="white")
        self.bottom_frame.pack(fill='both', side='bottom', padx=10, pady=10)
        self.confirm_btn = ButtonApp(self.bottom_frame, text="Confirm",
                                     command=self.manager.from_addstudy_to_studies_frame)
        self.back_btn = ButtonApp(self.bottom_frame, text="Back",
                                  command=self.manager.from_addstudy_to_studies_frame)
        self.confirm_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)
        self.back_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)

#-------------------------------------------------------------------#

class AddDaysOffTemplate(Frame):
    """
    Templates displayed when the user wants to add a study.
    """
    parameters = ["Title", "Operator", "Color"]
    def __init__(self, study_template) -> None:
        super().__init__(study_template)
        self.manager = study_template
        self.configure(bg="#FFFFFF")

        self.daysoff_title = LabelEntryPair(self, "Title")
        self.daysoff_title.pack(fill='both', side='top', padx=10)
        self.daysoff_operator = LabelEntryPair(self, "Operator")
        self.daysoff_operator.pack(fill='both', side='top', padx=10)

        ButtonApp(self, text="COLOR",
                  command=self.choose_color).pack(side="top")

        self.checkbox_var = IntVar()
        self.checkbox = Checkbutton(self, text="Force", bg="#FFFFFF", activebackground="#FFFFFF",
                               variable=self.checkbox_var, command=None)
        self.checkbox.pack(side='top', padx=10, pady=10, anchor="w")

        # agenda of the study
        self.agenda_canvas = Canvas(self, bg="gold")
        self.agenda_canvas.pack(fill='both', side='top', padx=10, pady=10)

        # Schedule picker
        self.schedule_selector = SchedulePicker(self)
        self.schedule_selector.pack(side="left")

        # Bottom widget
        self.bottom_frame = Frame(self, bg="white")
        self.bottom_frame.pack(fill='both', side='bottom', padx=10, pady=10)
        self.confirm_btn = ButtonApp(self.bottom_frame, text="Confirm",
                                     command=self.manager.from_adddaysoff_to_studies_frame)
        self.back_btn = ButtonApp(self.bottom_frame, text="Back",
                                  command=self.manager.from_adddaysoff_to_studies_frame)
        self.confirm_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)
        self.back_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)

    def choose_color(self) -> None:
        """
        Opens a color picker.
        returns the color chosen.
        """
        color = askcolor()
        if color:
            self.config(bg=color[1])

"""
qualifications.py

Frame containing the qualifications needed for a study.
"""

#------------------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, Label
from src.utils.graphical_utils import LabelEntryPair, IntVar, Checkbutton, ButtonApp, Entry

#------------------------------------------------------------------------------#

class QualificationTemplate(Frame):
    """
    Qualification page of the agenda.
    """
    def __init__(self, body:Frame) -> None:
        super().__init__(body)
        self.configure(bg='red')
        self.manager = body
        self.gui_manager = self.manager.manager.manager.gui
        self.db_cursor_manager = self.gui_manager.app.db_cursor
        self.qualification_examples = self.gui_manager.app.db_cursor.get_qualifications()
        self.configure(bg="white")
        self.propagate(False)


        self.qualifications_timeline = QualificationList(self)
        self.qualifications_timeline.pack(fill="both", expand=True, side="top")
        self.add_qualifications_template = None

    def from_timeline_to_add_qualifications(self):
        """
        Switches from the timeline to the add qualifications template.
        """
        if self.add_qualifications_template:
            self.add_qualifications_template.destroy()
        self.qualifications_timeline.pack_forget()
        self.setup_add_qualification()

    def from_add_qualifications_to_timeline(self):
        """
        Switches from the add qualifications template to the timeline.
        """
        self.add_qualifications_template.destroy()
        self.qualifications_timeline.pack(fill="both", expand=True, side="top")

    def setup_add_qualification(self):
        """
        Adds an qualification to the qualifications page.
        """
        self.add_qualifications_template = AddQualificationTemplate(self)
        self.add_qualifications_template.pack(fill='both', expand=True, side='top')

class QualificationList(Frame):
    """
    Contains qualifications names and their expiration dates
    in a timeline.
    """
    def __init__(self, manager=None) -> None:
        """
        Setup the lines of the qualifications page.
        Contains qualifications names on the left
        and their disponibilities on the right.
        """
        super().__init__(manager)
        self.manager = manager
        for qualification in self.manager.qualification_examples:
            line_frame = Frame(self)
            line_frame.propagate(False)
            line_frame.rowconfigure(0, weight=1)
            line_frame.columnconfigure(0, weight=1)
            line_frame.columnconfigure(1, weight=4)
            line_frame.pack(expand=True, side="top", fill="both")

            # Inside the line frame
            Label(line_frame, text=qualification["name"]).pack(side="left", fill="both")
            ButtonApp(line_frame, "Red", text="Details",
            command=lambda lf=line_frame, q=qualification:
                self.show_op_qualified(lf, q)).pack(side="right", fill="both")

    def show_op_qualified(self, frame:Frame, qualification:dict) -> None:
        """
        Shows the operators having the qualification.
        """
        operators_qualified = self.manager.db_cursor_manager.get_operators(
            qualification_id=qualification["id"])
        for operator in operators_qualified:
            text_var = f"{operator['name']} (expiration on {qualification['expiration_date']})"
            Label(frame,
                  text=text_var).pack(side="top", fill="both")



#-------------------------------------------------------------------#

class AddQualificationTemplate(Frame):
    """
    Add qualifications template.
    """
    def __init__(self, body=None):
        super().__init__(body)
        self.manager = body
        self.configure(bg="pink")
        self.propagate(False)

        self.setup_widgets()

    def setup_widgets(self) -> None:
        """
        Setup the widgets of the add qualifications template.
        """
        LabelEntryPair(self, "Qualification name").pack(fill="both", side="top")
        LabelEntryPair(self, "Rooms available").pack(fill="both", side="top")
        LabelEntryPair(self, "Constraint").pack(fill="both", side="top")
        Label(self, text="Description", bg="#FFFFFF").pack(side='top', padx=10)
        Entry(self, text="Description", width=10).pack(fill='both', side='top', padx=10)

        self.checkbox_var = IntVar()
        self.checkbox = Checkbutton(self, text="Archived", bg="#FFFFFF", activebackground="#FFFFFF",
                               variable=self.checkbox_var, command=None)
        self.checkbox.pack(side='top', padx=10, pady=10, anchor="w")

        # Bottom widget
        self.bottom_frame = Frame(self, bg="white")
        self.bottom_frame.pack(fill='both', side='bottom', padx=10, pady=10)
        self.confirm_btn = ButtonApp(self.bottom_frame, text="Confirm",
                                     command=None)
        self.back_btn = ButtonApp(self.bottom_frame, text="Back",
                                  command=self.manager.from_add_qualifications_to_timeline)
        self.confirm_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)
        self.back_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)

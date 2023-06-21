"""
operators.py

Contains the operators page.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, Label, Canvas, LabelEntryPair
from src.utils.graphical_utils import Checkbutton, IntVar, ButtonApp, Entry

#-------------------------------------------------------------------#

class OperatorsTemplate(Frame):
    """
    Contains the Frame in which will be displayed every
    templates related to the operators.
    """
    def __init__(self, body=None):
        super().__init__(body)
        self.manager = body
        self.operators_examples = self.manager.manager.manager.gui.app.db_cursor.get_operators()
        self.configure(bg="white")
        self.propagate(False)

        self.operators_timeline = OperatorsTimeline(self)
        self.operators_timeline.pack(fill="both", expand=True, side="top")
        self.add_operators_template = None

    def from_timeline_to_add_operators(self):
        """
        Switches from the timeline to the add operators template.
        """
        if self.add_operators_template:
            self.add_operators_template.destroy()
        self.operators_timeline.pack_forget()
        self.setup_add_operator()

    def from_add_operators_to_timeline(self):
        """
        Switches from the add operators template to the timeline.
        """
        self.add_operators_template.destroy()
        self.operators_timeline.pack(fill="both", expand=True, side="top")

    def setup_add_operator(self):
        """
        Adds an operator to the operators page.
        """
        self.add_operators_template = AddOperatorsTemplate(self)
        self.add_operators_template.pack(fill='both', expand=True, side='top')


class OperatorsTimeline(Frame):
    """
    Contains operators names and their disponibilities
    in a timeline.
    """
    def __init__(self, manager=None) -> None:
        """
        Setup the lines of the operators page.
        Contains operators names on the left
        and their disponibilities on the right.
        """
        super().__init__(manager)
        self.manager = manager
        for operators in self.manager.operators_examples:
            line_frame = Frame(self)
            line_frame.propagate(False)
            line_frame.rowconfigure(0, weight=1)
            line_frame.columnconfigure(0, weight=1)
            line_frame.columnconfigure(1, weight=4)
            line_frame.pack(fill="both", expand=True, side="top")
            Label(line_frame, text=operators["name"]).pack(side="left", fill="both")
            Canvas(line_frame, width=100,  height=100, bg="red").pack(side="right",
                                                                      fill="both",
                                                                      expand=True)

#-------------------------------------------------------------------#

class AddOperatorsTemplate(Frame):
    """
    Add operators template.
    """
    def __init__(self, body=None):
        super().__init__(body)
        self.manager = body
        self.configure(bg="white")
        self.propagate(False)

        self.setup_widgets()

    def setup_widgets(self) -> None:
        """
        Setup the widgets of the add operators template.
        """
        LabelEntryPair(self, "Operator name").pack(fill="both", side="top")
        LabelEntryPair(self, "Qualifications").pack(fill="both", side="top")

        self.checkbox_var = IntVar()
        self.checkbox = Checkbutton(self, text="Archived", bg="#FFFFFF", activebackground="#FFFFFF",
                               variable=self.checkbox_var, command=None)
        self.checkbox.pack(side='top', padx=10, pady=10, anchor="w")

        # Expiration qualifications
        self.expiration_qualifications = ExpirationQualifications(self)
        self.expiration_qualifications.pack(fill='both', side='top', expand=True)

        # Bottom widget
        self.bottom_frame = Frame(self, bg="white")
        self.bottom_frame.pack(fill='both', side='bottom', padx=10, pady=10)
        self.confirm_btn = ButtonApp(self.bottom_frame, text="Confirm",
                                     command=None)
        self.back_btn = ButtonApp(self.bottom_frame, text="Back",
                                  command=self.manager.from_add_operators_to_timeline)
        self.confirm_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)
        self.back_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)

class ExpirationQualifications(Frame):
    """
    Contains the expiration of the qualifications.
    """
    def __init__(self, add_operator_frame) -> None:
        super().__init__(add_operator_frame)
        self.configure(bg="white")
        self.manager = add_operator_frame
        self.operator_menu_manager = self.manager.manager.manager.manager.manager
        self.qualifications = self.operator_menu_manager.gui.app.db_cursor.get_qualifications()

        Label(self, text="Expiration date: ", bg="#FFFFFF",
              fg="#000000").pack(fill='both', side='left', pady=10)
        self.expiration_frame = Frame(self)
        self.expiration_frame.pack(fill='both', side='top', expand=True)

        for qualification in self.qualifications:
            QualificationLine(self.expiration_frame,
                              qualification["name"]).pack(fill='both',
                                                        side='top',
                                                        expand=True)

class QualificationLine(Frame):
    """
    Contains a qualification.
    """
    def __init__(self, expiration_qualifications_frame:Frame, qualification:str) -> None:
        super().__init__(expiration_qualifications_frame)
        self.manager = expiration_qualifications_frame
        self.qualification = qualification
        self.label = Label(self, text=f"{qualification} expired on ", fg="#000000", bg="#FFFFFF")
        self.label.pack(fill='both', side='left')
        self.entry = Entry(self)
        self.entry.pack(fill='both', side='left', expand=True)
        ButtonApp(self, text="reset", bg="#FFFFFF",
                  command=self.reset_qualification).pack(fill='both', side='left')

    def reset_qualification(self):
        """
        Resets the qualification.
        """
        self.entry.delete('0', 'end')
        self.entry.insert('0', self.qualification)

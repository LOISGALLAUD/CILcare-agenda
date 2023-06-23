"""
operators.py

Contains the operators page.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, Label, Canvas, LabelEntryPair, Scrollbar
from src.utils.graphical_utils import Checkbutton, IntVar, ButtonApp, DateEntry

#-------------------------------------------------------------------#

class OperatorsTemplate(Frame):
    """
    Contains the Frame in which will be displayed every
    templates related to the operators.
    """
    def __init__(self, body=None):
        super().__init__(body)
        self.manager = body
        self.db_cursor_manager = self.manager.manager.manager.gui.app.db_cursor
        self.operators_examples = self.db_cursor_manager.get_operators()
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

    def clear_timeline(self):
        """
        Clears the timeline.
        """
        for widget in self.operators_timeline.winfo_children():
            widget.destroy()

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
        self.setup_timeline()

    def setup_timeline(self):
        """
        setup the timeline.
        """
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
        self.name = LabelEntryPair(self, "Operator name")
        self.name.pack(fill="both", side="top")

        self.checkbox_var = IntVar()
        self.checkbox = Checkbutton(self, text="Archived", bg="#FFFFFF", activebackground="#FFFFFF",
                               variable=self.checkbox_var, command=None)
        self.checkbox.pack(side='top', padx=10, pady=10, anchor="w")

        # Expiration qualifications
        self.expiration_qualifications = ExpirationQualifications(self)
        self.expiration_qualifications.pack(fill='both', side='top', expand=True)

        # Qualifications allowed
        frame = Frame(self, bg="pink")
        frame.pack(side='left')
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        canvas = Canvas(frame, yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both")
        scrollbar.config(command=canvas.yview)
        inner_frame = Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor='nw')

        # Adding the checkboxes
        self.checkboxes = []
        for qual in self.manager.db_cursor_manager.get_qualifications():
            var = IntVar()
            checkbutton = Checkbutton(inner_frame, text=qual["name"],
                                      variable=var,
                                      command=self.expiration_qualifications.setup_qualifications)
            self.checkboxes.append((qual["id"], var))
            checkbutton.pack(anchor='w')
        inner_frame.bind('<Configure>',
                         lambda event: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>',
                    lambda event: canvas.configure(scrollregion=canvas.bbox('all')))

        # Bottom widget
        self.bottom_frame = Frame(self, bg="white")
        self.bottom_frame.pack(fill='both', side='bottom', padx=10, pady=10)
        self.confirm_btn = ButtonApp(self.bottom_frame, text="Confirm",
                                     command=self.confirm)
        self.back_btn = ButtonApp(self.bottom_frame, text="Back",
                                  command=self.manager.from_add_operators_to_timeline)
        self.confirm_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)
        self.back_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)

    def get_checked_vars(self) -> list:
        """
        Returns the checked vars of the checkboxes.
        """
        checked_vars = []
        for qual_id, var in self.checkboxes:
            if var.get():
                checked_vars.append(qual_id)
        return checked_vars

    def confirm(self) -> None:
        """
        Add the operator to the database.
        """
        name = self.name.entry.get()
        archived = self.checkbox_var.get()
        expiration_qualifications = self.expiration_qualifications.qualifications
        qualifications = self.get_checked_vars()
        qualif_selected = [item for item in expiration_qualifications
                           if item["id"] in qualifications]

        self.manager.db_cursor_manager.insert_operator(name, archived)
        new_operator = self.manager.db_cursor_manager.get_operators(name)[0]
        for qualif in qualif_selected:
            self.manager.db_cursor_manager.insert_link_operator_qualification(
                new_operator["id"], qualif['id'],
                self.expiration_qualifications.get_expiration_date(qualif["id"]))

        self.manager.operators_examples = self.manager.db_cursor_manager.get_operators()
        self.manager.clear_timeline()
        self.manager.operators_timeline.setup_timeline()
        self.manager.from_add_operators_to_timeline()

class ExpirationQualifications(Frame):
    """
    Contains the expiration of the qualifications.
    """
    def __init__(self, add_operator_frame) -> None:
        super().__init__(add_operator_frame)
        self.configure(bg="white")
        self.manager = add_operator_frame
        self.operator_menu_manager = self.manager.manager.manager.manager.manager
        self.qualifications = None

    def setup_qualifications(self) -> None:
        """
        Setup the qualifications.
        """
        self.clear_qualifications()
        checked_vars = self.manager.get_checked_vars()
        self.qualifications = self.operator_menu_manager.gui.app.db_cursor.get_qualifications()
        for qualification in self.qualifications:
            if any(qual_id == qualification["id"]
                   for qual_id in checked_vars):
                QualificationLine(self, qualification).pack(fill='both',
                                                                    side='top',
                                                                    expand=True)

    def clear_qualifications(self) -> None:
        """
        Clears the qualifications.
        """
        for qualification in self.winfo_children():
            qualification.destroy()

    def get_expiration_date(self, qualification_id:str) -> str:
        """
        Returns the date of the qualification.
        """
        for qualification_line in self.winfo_children():
            if qualification_line.qualification_id == qualification_id:
                return qualification_line.date_entry.get()
        return None

class QualificationLine(Frame):
    """
    Contains a qualification.
    """
    def __init__(self, expiration_qualifications_frame:Frame, qualification:dict) -> None:
        super().__init__(expiration_qualifications_frame)
        self.manager = expiration_qualifications_frame
        self.qualification_name = qualification["name"]
        self.qualification_id = qualification["id"]
        self.label = Label(self, text=f'{qualification["name"]} expire on ',
                           fg="#000000", bg="#FFFFFF")
        self.label.pack(fill='both', side='left')
        self.date_entry = DateEntry(self, width=20, background='#A91B60',
                                    foreground='white', borderwidth=2)
        self.date_entry.pack(fill='both', side='left')

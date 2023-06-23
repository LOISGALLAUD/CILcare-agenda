"""
template.py

This file contains the template template.
"""

#------------------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, Label, Canvas, Combobox
from src.utils.graphical_utils import LabelEntryPair, IntVar, Checkbutton, ButtonApp, Text, StringVar

#------------------------------------------------------------------------------#

class TemplatesTemplate(Frame):
    """
    Template page of the agenda.
    """
    def __init__(self, body:Frame) -> None:
        super().__init__(body)
        self.configure(bg='red')
        self.manager = body
        self.db_cursor_manager = self.manager.manager.manager.gui.app.db_cursor
        self.template_examples = self.db_cursor_manager.get_templates()
        self.configure(bg="white")
        self.propagate(False)

        self.templates_timeline = TemplateTimeline(self)
        self.templates_timeline.pack(fill="both", expand=True, side="top")
        self.add_templates_template = None

    def from_timeline_to_add_templates(self):
        """
        Switches from the timeline to the add templates template.
        """
        if self.add_templates_template:
            self.add_templates_template.destroy()
        self.templates_timeline.pack_forget()
        self.setup_add_template()

    def from_add_templates_to_timeline(self):
        """
        Switches from the add templates template to the timeline.
        """
        self.add_templates_template.destroy()
        self.templates_timeline.pack(fill="both", expand=True, side="top")

    def setup_add_template(self):
        """
        Adds an template to the templates page.
        """
        self.add_templates_template = AddTemplateTemplate(self)
        self.add_templates_template.pack(fill='both', expand=True, side='top')

    def clear_timeline(self):
        """
        Clears the timeline.
        """
        for child in self.templates_timeline.winfo_children():
            child.destroy()

class TemplateTimeline(Frame):
    """
    Contains templates names and their disponibilities
    in a timeline.
    """
    def __init__(self, manager=None) -> None:
        """
        Setup the lines of the templates page.
        Contains templates names on the left
        and their disponibilities on the right.
        """
        super().__init__(manager)
        self.manager = manager
        self.setup_timeline()

    def setup_timeline(self) -> None:
        """
        Setup the timeline of the templates page.
        """
        for template in self.manager.template_examples:
            line_frame = Frame(self)
            line_frame.propagate(False)
            line_frame.rowconfigure(0, weight=1)
            line_frame.columnconfigure(0, weight=1)
            line_frame.columnconfigure(1, weight=4)
            line_frame.pack(fill="both", expand=True, side="top")
            Label(line_frame, text=template["study_name"]).pack(side="left", fill="both")
            Canvas(line_frame, width=100,  height=100, bg="red").pack(side="right",
                                                                      fill="both",
                                                                      expand=True)

#-------------------------------------------------------------------#

class AddTemplateTemplate(Frame):
    """
    Add templates template.
    """
    def __init__(self, body=None):
        super().__init__(body)
        self.manager = body
        self.configure(bg="pink")
        self.propagate(False)

        self.setup_widgets()

    def setup_widgets(self) -> None:
        """
        Setup the widgets of the add templates template.
        """
        self.template_name = LabelEntryPair(self, "Template name")
        self.template_name.pack(fill="both", side="top")

        # animal_type widget
        options = [animal_type["name"] for
                   animal_type in self.manager.db_cursor_manager.get_animal_types()]
        self.animal_type = StringVar()
        Combobox(self, textvariable=self.animal_type, values=options,
                               state="readonly", width=30).pack()
        self.animal_type.set(options[0])

        Label(self, text="Description", bg="#FFFFFF").pack(side='top', padx=10)
        self.description = Text(self)
        self.description.pack(fill='both', side='top', padx=10)

        self.checkbox_var = IntVar()
        self.checkbox = Checkbutton(self, text="Archived", bg="#FFFFFF", activebackground="#FFFFFF",
                               variable=self.checkbox_var, command=None)
        self.checkbox.pack(side='top', padx=10, pady=10, anchor="w")

        # Bottom widget
        self.bottom_frame = Frame(self, bg="white")
        self.bottom_frame.pack(fill='both', side='bottom', padx=10, pady=10)
        self.confirm_btn = ButtonApp(self.bottom_frame, text="Confirm",
                                     command=self.confirm)
        self.back_btn = ButtonApp(self.bottom_frame, text="Back",
                                  command=self.manager.from_add_templates_to_timeline)
        self.confirm_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)
        self.back_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)

    def confirm(self):
        """
        Inserts a room in the database.
        """
        study_name = self.template_name.entry.get()
        archived = self.checkbox_var.get()
        animal_type_id = self.manager.db_cursor_manager.get_animal_types(
            self.animal_type.get())[0]["id"]
        description = self.description.get("1.0", "end-1c")

        self.manager.db_cursor_manager.insert_template(study_name, archived,
                                                       animal_type_id, description)

        self.manager.template_examples = self.manager.db_cursor_manager.get_templates()
        self.manager.clear_timeline()
        self.manager.templates_timeline.setup_timeline()
        self.manager.from_add_templates_to_timeline()

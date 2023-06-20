"""
animal_types.py

Page where the user will see every animal types
registered in the database.
"""

#------------------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, Label
from src.utils.graphical_utils import LabelEntryPair, ButtonApp, Entry

#------------------------------------------------------------------------------#

class AnimalTypeTemplate(Frame):
    """
    Animal Type page of the agenda.
    """
    def __init__(self, body:Frame) -> None:
        super().__init__(body)
        self.configure(bg='white')
        self.manager = body
        self.gui_manager = self.manager.manager.manager.gui
        self.db_cursor_manager = self.gui_manager.app.db_cursor
        self.animal_type_examples = self.gui_manager.app.db_cursor.get_animal_types()
        self.propagate(False)


        self.animal_types_timeline = AnimalTypeList(self)
        self.animal_types_timeline.pack(fill="both", expand=True, side="top")
        self.add_animal_types_template = None

    def from_timeline_to_add_animal_types(self):
        """
        Switches from the timeline to the add animal_types template.
        """
        if self.add_animal_types_template:
            self.add_animal_types_template.destroy()
        self.animal_types_timeline.pack_forget()
        self.setup_add_animal_type()

    def from_add_animal_types_to_timeline(self):
        """
        Switches from the add animal_types template to the timeline.
        """
        self.add_animal_types_template.destroy()
        self.animal_types_timeline.pack(fill="both", expand=True, side="top")

    def setup_add_animal_type(self):
        """
        Adds an animal_type to the animal_types page.
        """
        self.add_animal_types_template = AddAnimalTypeTemplate(self)
        self.add_animal_types_template.pack(fill='both', expand=True, side='top')

class AnimalTypeList(Frame):
    """
    Contains animal_types names and their expiration dates
    in a timeline.
    """
    def __init__(self, manager=None) -> None:
        """
        Setup the lines of the animal_types page.
        Contains animal_types names on the left
        and their disponibilities on the right.
        """
        super().__init__(manager)
        self.manager = manager
        for animal_type in self.manager.animal_type_examples:
            line_frame = Frame(self)
            line_frame.propagate(False)
            line_frame.rowconfigure(0, weight=1)
            line_frame.columnconfigure(0, weight=1)
            line_frame.columnconfigure(1, weight=4)
            line_frame.pack(expand=True, side="top", fill="both")

            # Inside the line frame
            Label(line_frame,
                  text=animal_type["name"]).pack(side="left", fill="both")

#-------------------------------------------------------------------#

class AddAnimalTypeTemplate(Frame):
    """
    Add animal_types template.
    """
    def __init__(self, body=None):
        super().__init__(body)
        self.manager = body
        self.configure(bg="pink")
        self.propagate(False)

        self.setup_widgets()

    def setup_widgets(self) -> None:
        """
        Setup the widgets of the add animal_types template.
        """
        LabelEntryPair(self, "Animal type name").pack(fill="both", side="top")
        Label(self, text="Description", bg="#FFFFFF").pack(side='top', padx=10)
        Entry(self, text="Description", width=10).pack(fill='both', side='top', padx=10)

        # Bottom widget
        self.bottom_frame = Frame(self, bg="white")
        self.bottom_frame.pack(fill='both', side='bottom', padx=10, pady=10)
        self.confirm_btn = ButtonApp(self.bottom_frame, text="Confirm",
                                     command=None)
        self.back_btn = ButtonApp(self.bottom_frame, text="Back",
                                  command=self.manager.from_add_animal_types_to_timeline)
        self.confirm_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)
        self.back_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)

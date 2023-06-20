"""
equipment.py

This file contains the equipment template.
"""

#------------------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, Label, Canvas
from src.utils.graphical_utils import LabelEntryPair, IntVar, Checkbutton, ButtonApp, Entry

#------------------------------------------------------------------------------#

class EquipmentTemplate(Frame):
    """
    Equipment page of the agenda.
    """
    def __init__(self, body:Frame) -> None:
        super().__init__(body)
        self.configure(bg='red')
        self.manager = body
        self.db_cursor_manager = self.manager.manager.manager.gui.app.db_cursor
        self.equipment_examples = self.db_cursor_manager.get_equipments()
        self.configure(bg="white")
        self.propagate(False)

        self.equipments_timeline = EquipmentTimeline(self)
        self.equipments_timeline.pack(fill="both", expand=True, side="top")
        self.add_equipments_template = None

    def from_timeline_to_add_equipments(self):
        """
        Switches from the timeline to the add equipments template.
        """
        if self.add_equipments_template:
            self.add_equipments_template.destroy()
        self.equipments_timeline.pack_forget()
        self.setup_add_equipment()

    def from_add_equipments_to_timeline(self):
        """
        Switches from the add equipments template to the timeline.
        """
        self.add_equipments_template.destroy()
        self.equipments_timeline.pack(fill="both", expand=True, side="top")

    def setup_add_equipment(self):
        """
        Adds an equipment to the equipments page.
        """
        self.add_equipments_template = AddEquipmentTemplate(self)
        self.add_equipments_template.pack(fill='both', expand=True, side='top')

class EquipmentTimeline(Frame):
    """
    Contains equipments names and their disponibilities
    in a timeline.
    """
    def __init__(self, manager=None) -> None:
        """
        Setup the lines of the equipments page.
        Contains equipments names on the left
        and their disponibilities on the right.
        """
        super().__init__(manager)
        self.manager = manager
        for equipment in self.manager.equipment_examples:
            line_frame = Frame(self)
            line_frame.propagate(False)
            line_frame.rowconfigure(0, weight=1)
            line_frame.columnconfigure(0, weight=1)
            line_frame.columnconfigure(1, weight=4)
            line_frame.pack(fill="both", expand=True, side="top")
            Label(line_frame, text=equipment["name"]).pack(side="left", fill="both")
            Canvas(line_frame, width=100,  height=100, bg="red").pack(side="right",
                                                                      fill="both",
                                                                      expand=True)

#-------------------------------------------------------------------#

class AddEquipmentTemplate(Frame):
    """
    Add equipments template.
    """
    def __init__(self, body=None):
        super().__init__(body)
        self.manager = body
        self.configure(bg="pink")
        self.propagate(False)

        self.setup_widgets()

    def setup_widgets(self) -> None:
        """
        Setup the widgets of the add equipments template.
        """
        self.equipment_name = LabelEntryPair(self, "Equipment name")
        self.equipment_name.pack(fill="both", side="top")

        LabelEntryPair(self, "Rooms available").pack(fill="both", side="top")
        LabelEntryPair(self, "Constraint").pack(fill="both", side="top")
        Label(self, text="Description", bg="#FFFFFF").pack(side='top', padx=10)
        self.description = Entry(self, text="Description", width=10)
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
                                  command=self.manager.from_add_equipments_to_timeline)
        self.confirm_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)
        self.back_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)

    def confirm(self):
        """
        Inserts a room in the database.
        """
        name = self.equipment_name.entry.get()
        archived = self.checkbox_var.get()
        description = self.description.get()

        self.manager.db_cursor_manager.insert_room(name, archived, description)
        self.manager.room_examples = self.manager.db_cursor_manager.get_rooms()
        self.manager.clear_timeline()
        self.manager.room_timeline.setup_timeline()
        self.manager.from_add_room_to_timeline()

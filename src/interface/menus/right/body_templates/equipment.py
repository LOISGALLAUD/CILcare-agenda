"""
equipment.py

This file contains the equipment template.
"""

#------------------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, Label, Canvas, Scrollbar, Radiobutton, Combobox
from src.utils.graphical_utils import LabelEntryPair, IntVar, Checkbutton, ButtonApp, Text, StringVar

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

    def clear_timeline(self):
        """
        Clears the timeline.
        """
        for child in self.equipments_timeline.winfo_children():
            child.destroy()

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
        self.setup_timeline()

    def setup_timeline(self) -> None:
        """
        Setup the timeline of the equipments page.
        """
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

        # Selection of the room
        frame = Frame(self)
        frame.pack(side='left')
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        canvas = Canvas(frame, yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both")
        scrollbar.config(command=canvas.yview)
        inner_frame = Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor='nw')

        # Adding the checkboxes
        self.selected_room_id = IntVar()
        for room in self.manager.db_cursor_manager.get_rooms():
            room_radio = Radiobutton(inner_frame,
                                     text=room["name"],
                                     value=room["id"],
                                     variable=self.selected_room_id)
            room_radio.pack(anchor='w')
        inner_frame.bind('<Configure>',
                         lambda event: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>',
                    lambda event: canvas.configure(scrollregion=canvas.bbox('all')))

        # Constraint widget
        options = ["Different animal types in the room",
                   "Privatize the room",
                   None]
        self.constraint = StringVar()
        Combobox(self, textvariable=self.constraint, values=options,
                               state="readonly", width=30).pack()

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
                                  command=self.manager.from_add_equipments_to_timeline)
        self.confirm_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)
        self.back_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)

    def get_constraint_id(self):
        """
        Given the str constraint return the int id of the constraint.
        """
        match self.constraint.get():
            case "Different animal types in the room":
                return 1
            case "Privatize the room":
                return 2
            case _:
                return None

    def confirm(self):
        """
        Inserts a room in the database.
        """
        name = self.equipment_name.entry.get()
        archived = self.checkbox_var.get()
        room_id = self.selected_room_id.get()
        constraint = self.get_constraint_id()
        description = self.description.get("1.0", "end-1c")

        self.manager.db_cursor_manager.insert_equipment(name, archived,  constraint, description)
        new_equipment = self.manager.db_cursor_manager.get_equipments(name)[0]
        self.manager.db_cursor_manager.insert_link_room_equipment(new_equipment["id"],
                                                                  room_id)

        self.manager.equipment_examples = self.manager.db_cursor_manager.get_equipments()
        self.manager.clear_timeline()
        self.manager.equipments_timeline.setup_timeline()
        self.manager.from_add_equipments_to_timeline()

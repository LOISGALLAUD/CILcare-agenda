"""
rooms.py

Contains the room page.
"""


#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, Label, Canvas, LabelEntryPair
from src.utils.graphical_utils import Checkbutton, IntVar, ButtonApp, Entry

#-------------------------------------------------------------------#

class RoomsTemplate(Frame):
    """
    Contains the Frame in which will be displayed every
    templates related to the rooms.
    """
    def __init__(self, body=None):
        super().__init__(body)
        self.manager = body
        self.configure(bg="white")
        self.room_examples = self.manager.manager.manager.gui.app.db_cursor.get_rooms()
        self.propagate(False)
        self.room_timeline = RoomsTimeline(self)
        self.room_timeline.pack(fill="both", expand=True, side="top")
        self.add_room_template = None

    def from_timeline_to_add_room(self):
        """
        Switches from the timeline to the add rooms template.
        """
        if self.add_room_template:
            self.add_room_template.destroy()
        self.room_timeline.pack_forget()
        self.setup_add_operator()

    def from_add_room_to_timeline(self):
        """
        Switches from the add rooms template to the timeline.
        """
        self.add_room_template.destroy()
        self.room_timeline.pack(fill="both", expand=True, side="top")

    def setup_add_operator(self):
        """
        Adds an operator to the rooms page.
        """
        self.add_room_template = AddRoomsTemplate(self)
        self.add_room_template.pack(fill='both', expand=True, side='top')

class RoomsTimeline(Frame):
    """
    Contains rooms names and their disponibilities
    in a timeline.
    """
    def __init__(self, manager=None) -> None:
        """
        Setup the lines of the rooms page.
        Contains rooms names on the left
        and their disponibilities on the right.
        """
        super().__init__(manager)
        self.manager = manager
        for rooms in self.manager.room_examples:
            line_frame = Frame(self)
            line_frame.propagate(False)
            line_frame.rowconfigure(0, weight=1)
            line_frame.columnconfigure(0, weight=1)
            line_frame.columnconfigure(1, weight=4)
            line_frame.pack(fill="both", expand=True, side="top")
            Label(line_frame, text=rooms["name"]).pack(side="left", fill="both")
            Canvas(line_frame, width=100,  height=100, bg="red").pack(side="right",
                                                                      fill="both",
                                                                      expand=True)

#-------------------------------------------------------------------#

class AddRoomsTemplate(Frame):
    """
    Add rooms template.
    """
    def __init__(self, body=None):
        super().__init__(body)
        self.manager = body
        self.configure(bg="white")
        self.propagate(False)

        self.setup_widgets()

    def setup_widgets(self) -> None:
        """
        Setup the widgets of the add rooms template.
        """
        LabelEntryPair(self, "Room name").pack(fill="both", side="top")

        self.checkbox_var = IntVar()
        self.checkbox = Checkbutton(self, text="Archived", bg="#FFFFFF", activebackground="#FFFFFF",
                               variable=self.checkbox_var, command=None)
        self.checkbox.pack(side='top', padx=10, pady=10, anchor="w")

        self.description = Entry(self, width=50)
        self.description.pack(fill="both", side="top", padx=10, pady=10)

        # Bottom widget
        self.bottom_frame = Frame(self, bg="white")
        self.confirm_btn = ButtonApp(self.bottom_frame, text="Confirm",
                                     command=self.insert_room)
        self.back_btn = ButtonApp(self.bottom_frame, text="Back",
                                  command=self.manager.from_add_room_to_timeline)

        self.bottom_frame.pack(fill='both', side='bottom', padx=10, pady=10)
        self.confirm_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)
        self.back_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)

    def insert_room(self):
        """
        Inserts a room in the database.
        """


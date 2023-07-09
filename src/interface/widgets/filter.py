"""
filtrer.py

Widget that allows to filter the task by category.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, Combobox, StringVar
from src.utils.graphical_utils import ButtonApp, Label, Checkbutton, IntVar

#-------------------------------------------------------------------#

class LabelComboPair(Frame):
    """
    A pair of a label and a combobox
    """
    def __init__(self, master, text, values):
        """
        Constructor of the LabelComboPair class.
        """
        super().__init__(master, bg="#5b557f")
        self.master = master
        self.rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, uniform="group")
        self.grid_columnconfigure(1, weight=2, uniform="group")
        self.label = Label(self, text=text, bg="#5b557f", fg="white")
        self.label.grid(row=0, column=0, sticky="nsew")
        constraint=StringVar()
        self.combobox = Combobox(self, textvariable=constraint, values=values, state
                                    ="readonly", width=15)
        self.combobox.set(text)
        self.combobox.grid(row=0, column=1, sticky="nsew")

class Filters(Frame):
    """
    Widget that allows to filter the task by category.
    """
    def __init__(self, master):
        """
        Constructor of the Filters class.
        """
        super().__init__(master, bg="#494466")
        self.master = master
        self.db_manager = self.master.master.manager.gui.app.db_cursor
        Label(self, text="Filters", bg="#494466",
              fg="white").pack(side='top', fill="both", expand=True)

        self.confirm_filtering_btn = ButtonApp(self, text="Confirm filters", custom_theme="Green",
                                                  command=self.confirm_filtering)
        self.confirm_filtering_btn.pack(side="right", fill="both", expand=True)

        combos_frame = Frame(self, bg="#494466")
        combos_frame.pack(side="left")

        self.archived = IntVar()
        self.filter_archived = Checkbutton(self, text="Show Archived",
                                           bg="white",
                                           highlightbackground="#494466",
                                           highlightcolor="#494466",
                                           highlightthickness=0,
                                           variable=self.archived)
        self.filter_archived.pack(side="left", padx=10)

        up_frame = Frame(combos_frame, bg="#494466")
        study_options = ["All", "CILcare", "CILcare - CILcare"]
        self.study_category = LabelComboPair(up_frame, "Study", study_options)
        self.study_category.pack(side="left", padx=5, fill="both", expand=True)

        equipment_options = [eqpt["name"] for eqpt in self.db_manager.get_equipments()]
        self.equipment_category = LabelComboPair(up_frame, "Equipment", equipment_options)
        self.equipment_category.pack(side="left", padx=5, fill="both", expand=True)

        bottom_frame = Frame(combos_frame, bg="#494466")
        room_options = [room["name"] for room in self.db_manager.get_rooms()]
        self.room_category = LabelComboPair(bottom_frame, "Room", room_options)
        self.room_category.pack(side="left", padx=5, fill="both", expand=True)

        op_options = [op["name"] for op in self.db_manager.get_operators()]
        self.operator_category = LabelComboPair(bottom_frame, "Operators", op_options)
        self.operator_category.pack(side="left", padx=5, fill="both", expand=True)

        up_frame.pack(side="top", padx=5, pady=5)
        bottom_frame.pack(side="top", padx=5, pady=5)


    def confirm_filtering(self):
        """
        Confirm the filtering.
        """
        # self.master.study_manager.filter_tasks(self.constraint.get())

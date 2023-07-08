"""
footer.py

Describes the footer of the shopping menu.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, Checkbutton, IntVar, Label
from src.interface.widgets.schedule_picker import SchedulePicker
from src.interface.widgets.filter import Filters

#-------------------------------------------------------------------#

class Footer(Frame):
    """
    Footer of the shopping menu.
    Contains the confirm button and the reset button
    and the total of the cart.
    """
    def __init__(self, manager=None):
        super().__init__(manager)
        self.manager = manager
        self.grid(row=2, column=0, sticky='nsew')
        self.update_idletasks()
        self.study_manager = manager.manager
        self.loggers = self.study_manager.gui.app.loggers
        self.grid_propagate(False)
        self.configure(bg="#8c77ff")

        self.schedule_picker = SchedulePicker(self)
        self.schedule_picker.pack(side="left", padx=10)
        self.archived = IntVar()
        self.filter_archived = Checkbutton(self, text="Show Archived",
                                           bg="white",
                                           highlightbackground="#8c77ff",
                                           highlightcolor="#8c77ff",
                                           highlightthickness=0,
                                           variable=self.archived,
                                           command=self.filter_archived_tasks)
        self.filter_archived.pack(side="left", padx=10)

        self.filters = Filters(self)
        self.filters.pack(side="left", padx=10)

        logo_label = Label(self, image=self.study_manager.gui.cilcare_logo,
                           border=0, bg="#8c77ff", highlightthickness=0)
        logo_label.place(relx=1.0, rely=1.0, anchor="se")

    def filter_archived_tasks(self):
        """
        Filter the archived tasks.
        """
        self.loggers.log.debug("Filter archived tasks")
        # self.study_manager.filter_archived_tasks(self.archived.get())

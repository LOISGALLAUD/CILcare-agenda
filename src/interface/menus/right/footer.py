"""
footer.py

Describes the footer of the shopping menu.
"""

# -------------------------------------------------------------------#

from src.utils.graphical_utils import Frame
from src.interface.widgets.schedule_picker import SchedulePicker
from src.interface.widgets.filter import Filters

# -------------------------------------------------------------------#


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
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=5)
        # self.grid_columnconfigure(2, weight=1)
        self.configure(bg="#8c77ff")

        self.schedule_picker = SchedulePicker(self)
        self.filters = Filters(self)

        self.show_filters()

    def filter_archived_tasks(self):
        """
        Filter the archived tasks.
        """
        self.loggers.log.debug("Filter archived tasks")
        # self.study_manager.filter_archived_tasks(self.archived.get())

    def show_filters(self):
        """
        Show the filters.
        """
        self.filters.grid(row=0, column=1, sticky="nsew",
                          padx=(0, 5), pady=(0, 10))
        self.schedule_picker.grid(
            row=0, column=0, sticky="nsew", padx=(0, 5), pady=(0, 10))

    def hide_filters(self):
        """
        Hide the filters.
        """
        self.filters.grid_forget()
        self.schedule_picker.grid_forget()

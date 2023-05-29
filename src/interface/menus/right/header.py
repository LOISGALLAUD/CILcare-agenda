"""
header.py

Top section of the shopping menu.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, ButtonApp

#-------------------------------------------------------------------#


class Header(Frame):
    """
    Top section of the shopping menu.
    """
    def __init__(self, manager=None) -> None:
        super().__init__(manager)
        self.manager = manager

        self.grid_propagate(False)
        self.configure(bg="#2bb5a6")
        self.setup_widgets()

    def setup_widgets(self) -> bool:
        """
        Setup the widgets of the header.
        """
        self.add_study_btn = ButtonApp(self, "Green", text="Add study",
                                       command=None)
        self.add_days_off_btn = ButtonApp(self, "Green", text="Add days off",
                                            command=None)

        self.add_study_btn.pack(side="left", fill="x", expand=True,
                                padx=10, pady=10)
        self.add_days_off_btn.pack(side="left", fill="x", expand=True,
                                   padx=10, pady=10)
        return True

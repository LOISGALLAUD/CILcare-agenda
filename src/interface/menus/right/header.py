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
    toggles = ["Add study", "Add days off"]
    def __init__(self, manager=None) -> None:
        super().__init__(manager)
        self.manager = manager
        # Default toggle
        self.current_toggle = None
        self.grid_propagate(False)
        self.configure(bg="#2bb5a6")
        self.setup_widgets()

    def setup_widgets(self) -> bool:
        """
        Setup the widgets of the header.
        """

        self.add_study_btn = ButtonApp(self, "Green", text="Add study",
                                       command=lambda: self.toggle("Add study"))
        self.add_days_off_btn = ButtonApp(self, "Green", text="Add days off",
                                            command=lambda: self.toggle("Add days off"))

        self.add_study_btn.pack(side="left", fill="x", expand=True,
                                padx=10, pady=10)
        self.add_days_off_btn.pack(side="left", fill="x", expand=True,
                                   padx=10, pady=10)
        return True

    def toggle(self, toggle: str) -> None:
        """
        Changes the current toggle of the navbar.
        """
        if toggle is None:
            for toggle in self.toggles:
                button = getattr(self, f"{toggle.lower().replace(' ', '_')}_btn")
                button.configure(bg=ButtonApp.DEFAULT_BG_GREEN)
            return

        self.current_toggle = toggle
        # Update button's colors
        for toggle in self.toggles:
            btn_name = toggle.lower().replace(" ", "_")
            button = getattr(self, f"{btn_name}_btn")
            if toggle == self.current_toggle:
                button.configure(bg=ButtonApp.ACTIVE_TOGGLE_GREEN)  # set active toggle color
            else:
                button.configure(bg=ButtonApp.DEFAULT_BG_GREEN)  # set default color

        # <update body>

    def reset_modifications(self) -> None:
        """
        Resets the modifications made by the user.
        """
        self.toggle(None)

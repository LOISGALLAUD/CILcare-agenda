"""
Nabar.py

Configure MarcoNeo's navbar on its shopping menu.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, ButtonApp

#-------------------------------------------------------------------#

class Navbar(Frame):
    """
    Contains the different toggles of the shopping menu.
    Is used to navigate between the different toggles.
    """
    def __init__(self, left_grid=None) -> None:
        super().__init__(left_grid)
        self.manager = left_grid
        # Default toggle
        self.current_toggle = "Studies"
        self.disconnect_btn = None

        self.grid_propagate(False)
        self.configure(bg="#6F2DA8")
        self.setup_buttons()

    def setup_buttons(self) -> bool:
        """
        Defines the buttons used in the menu.
        """
        toggles = ["Studies", "Operators", "Equipment",
                   "Rooms", "Qualifications", "Animal types",
                   "Templates"]
        row = 1
        for toggle in toggles:
            button = ButtonApp(self, text=toggle,
                               command=lambda toggle=toggle: self.toggle(toggle))
            setattr(self, f"{toggle.lower()}_btn", button)
            button.grid(row=row, column=0, padx=10, pady=10)
            row += 1

        self.disconnect_btn = ButtonApp(self, text="Disconnect",
                                  command=None)
        self.export_btn = ButtonApp(self, text="Export",
                                    command=None)

        self.disconnect_btn.grid(row=row, column=0, padx=10, pady=10)
        return True

    def toggle(self, toggle: str) -> None:
        """
        Changes the current toggle of the navbar.
        """
        self.current_toggle = toggle

        # <update right_grid>

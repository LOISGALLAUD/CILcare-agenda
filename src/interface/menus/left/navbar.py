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
        self.configure(bg="#F40B7C")
        self.setup_buttons()

    def setup_buttons(self) -> bool:
        """
        Defines the buttons used in the menu.
        """
        toggles = ["Studies", "Operators", "Equipment",
                   "Rooms", "Qualifications", "Animal types",
                   "Templates"]
        for toggle in toggles:
            button = ButtonApp(self, text=toggle,
                               command=lambda toggle=toggle: self.toggle(toggle))
            setattr(self, f"{toggle.lower()}_btn", button)
            button.pack(fill='both', expand=True, side='top', padx=10, pady=10)

        self.export_btn = ButtonApp(self, text="Export",
                                    command=None)
        self.disconnect_btn = ButtonApp(self, text="Disconnect",
                                  command=self.manager.manager.gui.app.close)

        self.export_btn.pack(fill='both', expand=True, side='top', padx=10, pady=10)
        self.disconnect_btn.pack(fill='both', expand=True, side='top', padx=10, pady=10)
        return True

    def toggle(self, toggle: str) -> None:
        """
        Changes the current toggle of the navbar.
        """
        self.current_toggle = toggle

        # <update right_grid>

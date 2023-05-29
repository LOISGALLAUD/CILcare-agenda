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
    toggles = ["Studies", "Operators", "Equipment",
                   "Rooms", "Qualifications", "Animal types",
                   "Templates"]
    def __init__(self, left_grid=None) -> None:
        super().__init__(left_grid)
        self.manager = left_grid
        # Default toggle
        self.current_toggle = "Studies"

        self.grid_propagate(False)
        self.configure(bg="#F40B7C")
        self.setup_buttons()
        self.toggle(self.current_toggle)

    def setup_buttons(self) -> bool:
        """
        Defines the buttons used in the menu.
        """
        for toggle in self.toggles:
            button = ButtonApp(self, text=toggle.upper(),
                               command=lambda toggle=toggle: self.toggle(toggle))
            setattr(self, f"{toggle.lower()}_btn", button)
            button.pack(fill='both', expand=True, side='top', padx=10, pady=10)

        self.export_btn = ButtonApp(self, text="EXPORT",
                                    command=None)
        self.disconnect_btn = ButtonApp(self, text="DISCONNECT",
                                  command=self.disconnect)

        self.export_btn.pack(fill='both', expand=True, side='top', padx=10, pady=10)
        self.disconnect_btn.pack(fill='both', expand=True, side='bottom', padx=10, pady=(100, 10))
        return True

    def toggle(self, toggle: str) -> None:
        """
        Changes the current toggle of the navbar.
        """
        self.current_toggle = toggle

        # Update button's colors
        for toggle in self.toggles:
            button = getattr(self, f"{toggle.lower()}_btn")
            if toggle == self.current_toggle:
                button.configure(bg=ButtonApp.ACTIVE_TOGGLE_COLOR)  # set active toggle color
            else:
                button.configure(bg=ButtonApp.DEFAULT_BG)  # set default color

        # <update right_grid>

    def disconnect(self) -> None:
        """
        Disconnects the user.
        """
        self.manager.manager.gui.change_menu(self.manager.manager.gui.login_menu)

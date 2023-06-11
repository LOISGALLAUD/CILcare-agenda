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
        self.current_toggle = self.toggles[0]

        self.grid_propagate(False)
        self.configure(bg="#F40B7C")
        self.setup_buttons()

    def setup_buttons(self) -> bool:
        """
        Defines the buttons used in the menu.
        """
        buttons = []
        for toggle in self.toggles:
            button = ButtonApp(self, text=toggle.upper(),
                               command=lambda toggle=toggle: self.toggle(toggle))
            setattr(self, f"{toggle.lower()}_btn", button)
            button.pack(fill='both', expand=True, side='top', padx=10, pady=10)
            buttons.append(button)
        if buttons:
            buttons[0].configure(bg=ButtonApp.ACTIVE_TOGGLE_RED)  # set active toggle color


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
        Updates the right_grid accordingly.
        """
        self.current_toggle = toggle

        # Update button's colors
        for toggle in self.toggles:
            button = getattr(self, f"{toggle.lower()}_btn")
            if toggle == self.current_toggle:
                button.configure(bg=ButtonApp.ACTIVE_TOGGLE_RED)  # set active toggle color
            else:
                button.configure(bg=ButtonApp.DEFAULT_BG_RED)  # set default color

        self.manager.manager.right_grid.body.update_body(self.current_toggle)
        self.manager.manager.right_grid.header.update_header(self.current_toggle)

    def disconnect(self) -> None:
        """
        Disconnects the user.
        """
        self.reset_mofifications()
        self.manager.manager.right_grid.reset_modifications()
        self.manager.manager.gui.change_menu(self.manager.manager.gui.login_menu)

    def reset_mofifications(self) -> None:
        """
        Resets the modifications made by the navbar.
        """
        current_toggle = "Studies"
        self.toggle(current_toggle)

"""
main_menu.py

Configure the main menu of the application.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, Label, BOTH, ButtonApp

#-------------------------------------------------------------------#

class MainMenu(Frame):
    """
    Agenda's main page.

    It is the first page to appear when the user logs in.
    """
    def __init__(self, gui=None) -> None:
        super().__init__(gui)
        self.gui = gui

        self.setup_label()
        self.setup_buttons()

    def setup_label(self) -> bool:
        """
        Defines the labels used in the main menu.
        """
        self.welcome_label = Label(self, text="Welcome to Agenda")
        self.welcome_label.pack(fill=BOTH)
        return True

    def setup_buttons(self):
        """
        Defines the buttons used in the main menu.
        """
        self.enter_btn = ButtonApp(self, text="Enter",
                                   command=lambda: self.gui.change_menu(self.gui.main_menu))
        self.help_btn = ButtonApp(self, text="Help",
                                     command=lambda: self.gui.change_menu(self.gui.help_menu))
        self.power_btn = ButtonApp(self, text="Power off",
                                   command=self.gui.app.close)

        for btn in [self.enter_btn, self.help_btn, self.power_btn]:
            btn.pack()

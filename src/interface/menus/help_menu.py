"""
help_menu.py

This module defines the HelpMenu class.
Defines the menu to display the help of
the application.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, Label, Button, TOP, BOTTOM, BOTH

#-------------------------------------------------------------------#

class HelpMenu(Frame):
    """
    Help menu of the application.
    """
    def __init__(self, gui) -> None:
        super().__init__(gui)
        self.gui = gui
        self.loggers = gui.loggers
        self.config(bg="black")
        self.setup_widgets()

    def setup_widgets(self) -> bool:
        """
        Setup the widgets of the menu.
        """
        self.loggers.log.debug("Setting up the widgets of the help menu...")

        self.help_label = Label(self, text="Help menu", bg="black", fg="white")
        self.help_label.pack(side=TOP, fill=BOTH, expand=True)

        self.tips_label = Label(self, text=tips_text, bg="black", fg="white")
        self.tips_label.pack(side=TOP, fill=BOTH, expand=True)

        self.back_button = Button(self, text="Back", bg="black", fg="white",
                                  command=lambda: self.gui.change_menu(self.gui.main_menu))
        self.back_button.pack(side=BOTTOM, fill=BOTH, expand=True)
        return True

tips_text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ac
ultricies nulla, et aliquet justo. Fusce sit amet risus metus. Quisque sollicitudin
a elit scelerisque efficitur. Integer laoreet dui sed lacus pellentesque, ac cursus
magna viverra. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices
posuere cubilia curae; Suspendisse sodales blandit nulla, sed ullamcorper lectus
tempor in. Nunc sit amet ligula suscipit, dictum mi eu, suscipit ante. Etiam tempor
felis quis nunc porttitor, nec facilisis velit interdum. Proin volutpat semper augue
eget eleifend. Nullam et dolor semper, dictum nibh et, sollicitudin erat."""
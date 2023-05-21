"""
login_menu.py

This module defines the LoginMenu class
to manage the login menu of the application.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, Button, BOTH, EntryApp, Label

#-------------------------------------------------------------------#

class LoginMenu(Frame):
    """
    Login menu of the application.
    Is the first menu displayed when
    launching the application.
    """
    def __init__(self, gui=None) -> None:
        super().__init__(gui)
        self.gui = gui
        self.config(bg="red")

        self.app_name_label = None
        self.login_button = None
        self.username_entry = None
        self.password_entry = None

        self.setup_images()
        self.setup_label()
        self.setup_entry()
        self.setup_buttons()

    def setup_images(self) -> bool:
        """
        Setup the images of the menu.
        """
        return True

    def setup_label(self) -> bool:
        """
        Setup the label of the menu.
        """
        self.app_name_label = Label(self, text=self.gui.app.NAME,
                                    fg="white", bg="black")
        self.app_name_label.pack(fill=BOTH, expand=True)
        return True

    def setup_buttons(self) -> bool:
        """
        Setup the buttons of the menu.
        Returns True if setup was successful.
        """
        self.login_button = Button(self, text="Login",
                                   command=self.log_in)
        self.login_button.bind("<Return>", self.log_in)
        self.login_button.pack(fill=BOTH, expand=True)
        return True

    def setup_entry(self) -> bool:
        """
        Setup the entry of the menu.
        Returns True if setup was successful.
        """
        self.username_entry = EntryApp("username", self)
        self.username_entry.pack(fill=BOTH, expand=True)

        self.password_entry = EntryApp("password", self, show='•')
        self.password_entry.pack(fill=BOTH, expand=True)

        return True

    def log_in(self, _event) -> bool:
        """
        Logs the user in.
        Returns True if login was successful.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "admin" and password == "admin":
            self.gui.current_menu = self.gui.main_menu
            self.gui.current_menu.pack(fill=BOTH, expand=True)
            self.pack_forget()
            return True
        return False

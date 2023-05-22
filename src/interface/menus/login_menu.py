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
        self.config(bg="gray")
        self.login_container = LoginContainer(self)
        self.login_container.pack()
        self.setup_images()

    def setup_images(self) -> bool:
        """
        Setup the images of the menu.
        """
        return True

    def log_in(self) -> bool:
        """
        Logs the user in.
        Returns True if login was successful.
        """
        username = self.login_container.username_entry.get()
        password = self.login_container.pwd_entry.get()
        if username == "admin" and password == "admin":
            self.gui.current_menu = self.gui.main_menu
            self.gui.current_menu.pack(fill=BOTH, expand=True)
            self.pack_forget()
            return True
        return False

class LoginContainer(Frame):
    """
    Container of the login menu.
    """
    def __init__(self, parent_menu=None) -> None:
        super().__init__(parent_menu)
        self.parent_menu = parent_menu

        self.setup_widgets()

    def setup_widgets(self) -> bool:
        """
        Setup the widgets of the container.
        """
        self.username_label = Label(self, text="Enter your username:", font=("system", 20))
        self.username_label.pack(fill=BOTH, expand=True)
        self.username_entry = EntryApp("username", False, self)
        self.username_entry.pack(fill=BOTH, expand=True)
        self.pwd_label = Label(self, text="Enter your password:", font=("system", 20))
        self.pwd_label.pack(fill=BOTH, expand=True)
        self.pwd_entry = EntryApp("password", True, self, show='•')
        self.pwd_entry.pack(fill=BOTH, expand=True)

        self.login_button = Button(self, text="Login",
                                      command=self.parent_menu.log_in)
        self.login_button.pack(fill=BOTH, expand=True)

        return True

"""
login_menu.py

This module defines the LoginMenu class
to manage the login menu of the application.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, BOTH, EntryApp, ButtonApp, Label

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
        self.config(bg="#FFFFFF")

        self.login_container = LoginContainer(self)
        self.name_to_display = self.gui.app.NAME.replace("_", " ")
        self.name_label = Label(self, text=self.name_to_display,
                                font=("System", 30), bg="#FFFFFF", fg="black")
        self.wrong_label = LoginErrorLabel(self, text="Wrong username or password")

        self.name_label.pack(pady=(100, 0))
        self.login_container.pack(pady=(150, 0))

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

        _oid, _username, _password, _qualifications = self.gui.app.db_cursor.get_user(username)

        if password == _password:
            self.gui.change_menu(self.gui.main_menu)
            self.login_container.username_entry.reset()
            self.login_container.pwd_entry.reset()
            self.wrong_label.pack_forget()
            return True

        self.login_container.pwd_entry.reset()
        self.wrong_label.pack(pady=50)
        return False

class LoginContainer(Frame):
    """
    Container of the login menu.
    """
    def __init__(self, parent_menu=None) -> None:
        super().__init__(parent_menu)
        self.parent_menu = parent_menu
        self.config(bg="#F40B7C", relief="groove", bd=20)
        self.setup_widgets()

    def setup_widgets(self) -> bool:
        """
        Setup the widgets of the container.
        """
        self.username_entry = EntryApp("username", False, self)
        self.pwd_entry = EntryApp("password", True, self, show='•')
        self.login_button = ButtonApp(self, text="Login",
                                      command=self.parent_menu.log_in)
        self.quit_btn = ButtonApp(self, text="Quit",
                               command=self.parent_menu.gui.app.close)

        self.username_entry.pack(fill=BOTH, expand=True, pady=(50, 10), padx=20)
        self.pwd_entry.pack(fill=BOTH, expand=True, pady=(10, 50), padx=20)
        self.login_button.pack(fill=BOTH, expand=True, pady=(0, 30), padx=150)
        self.quit_btn.pack(fill=BOTH, expand=True, pady=(0, 30), padx=150)
        return True

class LoginErrorLabel(Label):
    """
    Label displayed when
    login is unsuccessful.
    """
    def __init__(self, parent_menu=None, text:str=None) -> None:
        super().__init__(parent_menu)
        self.parent_menu = parent_menu
        self.config(bg="#F40B7C", fg="white", font=("System", 12), text=text.upper())

"""
button_app.py

Configure application's buttons.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Button

#-------------------------------------------------------------------#

class ButtonApp(Button):
    """
    Application's button.
    """
    DEFAULT_BG_RED = "#8c77ff"
    DEFAULT_BG_GREEN = "#494466"
    ACTIVE_TOGGLE_RED = "#a191ff"
    ACTIVE_TOGGLE_GREEN = "#5b557f"
    def __init__(self, master=None, custom_theme:str="Red", **kwargs) -> None:
        Button.__init__(self, master, **kwargs)

        if custom_theme == "Red":
            self.configure(font=("System", 12), bg=self.DEFAULT_BG_RED,
                            fg="#FFFFFF", activebackground="#a191ff",
                            activeforeground="#FFFFFF", bd=0, highlightthickness=10,
                            highlightbackground=self.ACTIVE_TOGGLE_RED,
                            relief="flat", padx=10, pady=10)
        elif custom_theme == "Green":
            self.configure(font=("System", 12), bg=self.DEFAULT_BG_GREEN,
                            fg="#FFFFFF", activebackground="#5b557f",
                            activeforeground="#FFFFFF", bd=0, highlightthickness=10,
                            highlightbackground=self.ACTIVE_TOGGLE_GREEN,
                            relief="flat", padx=10, pady=10)

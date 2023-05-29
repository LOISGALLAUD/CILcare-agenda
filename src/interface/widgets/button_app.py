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
    DEFAULT_BG_RED = "#A91B60"
    DEFAULT_BG_GREEN = "#057A6D"
    ACTIVE_TOGGLE_RED = "#900C3F"
    ACTIVE_TOGGLE_GREEN = "#0B5345"
    def __init__(self, master=None, custom_theme:str="Red", **kwargs) -> None:
        Button.__init__(self, master, **kwargs)

        if custom_theme == "Red":
            self.configure(font=("System", 12), bg="#A91B60",
                            fg="#FFFFFF", activebackground="#DE026D",
                            activeforeground="#FFFFFF", bd=0, highlightthickness=0,
                            relief="flat", padx=10, pady=10)
        elif custom_theme == "Green":
            self.configure(font=("System", 12), bg="#057A6D",
                            fg="#FFFFFF", activebackground="#019887",
                            activeforeground="#FFFFFF", bd=0, highlightthickness=0,
                            relief="flat", padx=10, pady=10)

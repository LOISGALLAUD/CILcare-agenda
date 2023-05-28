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
    DEFAULT_BG = "#A91B60"
    ACTIVE_TOGGLE_COLOR = "#2bb5a6"
    def __init__(self, master=None, **kwargs) -> None:
        Button.__init__(self, master, **kwargs)
        self.configure(font=("System", 12), bg="#A91B60",
                       fg="#FFFFFF", activebackground="#DE026D",
                       activeforeground="#FFFFFF", bd=0, highlightthickness=0,
                       relief="flat", padx=10, pady=10)

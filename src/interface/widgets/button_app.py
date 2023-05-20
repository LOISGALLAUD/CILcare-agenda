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
    def __init__(self, master=None, **kwargs) -> None:
        Button.__init__(self, master, **kwargs)
        self.configure(font=("System", 12), bg="#333333",
                       fg="#FFFFFF", activebackground="#555555",
                       activeforeground="#FFFFFF", bd=0, highlightthickness=0,
                       relief="flat", padx=10, pady=10)

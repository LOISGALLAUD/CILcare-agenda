"""
entry_app.py

Defines the custom Entry class for
the application.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Entry

#-------------------------------------------------------------------#

class EntryApp(Entry):
    """
    Custom Entry class for the application.
    """
    focused_entry = None

    def __init__(self, name:str, hidden:bool, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.name = name
        self.hidden = hidden

        self.config(bg="lightgray", fg="gray", insertbackground="white", font=("system", 15))
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

        self.on_focus_out(None)

    def on_focus_in(self, _event:object) -> None:
        """
        When the entry is focused, the text is deleted.
        """
        EntryApp.focused_entry = self
        if self.get() == self.name:
            self.delete(0, "end")
            self.config(fg='white')

        if self.hidden:
            self.config(show='•')

    def on_focus_out(self, _event:object) -> None:
        """
        When the entry is unfocused, the text is set to
        either "username" or "password". It depends on the
        name of the entry.
        """
        EntryApp.focused_entry = None
        if self.get() == "":
            self.insert(0, self.name)
            self.config(fg='white', show='')

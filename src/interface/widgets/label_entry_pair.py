"""
label_entry_pair.py

Contains the LabelEntryPair widget
which is a Label and an Entry.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, EntryApp, Label

#-------------------------------------------------------------------#

class LabelEntryPair(Frame):
    """
    Templates containing a label and an entry.
    """
    def __init__(self, master=None, text:str="", **kwargs) -> None:
        Frame.__init__(self, master, **kwargs)
        self.configure(bg="#FFFFFF")
        self.label = Label(self, text=text+":", bg="#FFFFFF", fg="#000000")
        self.entry = self.pwd_entry = EntryApp(text, False, self)
        self.label.pack(side='left', padx=10, pady=10)
        self.entry.pack(side='left', padx=10, pady=10)

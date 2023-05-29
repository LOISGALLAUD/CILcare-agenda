"""
gui_utils.py

Defines the tkinter classes that are used in the application.
Helps to reduce the number of imports in the other files.
"""

#-------------------------------------------------------------------#

from tkinter import Tk, Frame, TOP, BOTTOM, BOTH, Button, Entry, Label, Canvas
from src.interface.widgets.entry_app import EntryApp
from src.interface.widgets.button_app import ButtonApp
from src.interface.widgets.label_entry_pair import LabelEntryPair

#-------------------------------------------------------------------#

__all__ = ['Tk', 'Frame', 'TOP', 'BOTTOM', 'BOTH', 'Button',
           'Entry', 'Canvas', 'Label', 'EntryApp', 'ButtonApp',
           'LabelEntryPair']

"""
gui_utils.py

Defines the tkinter classes that are used in the application.
Helps to reduce the number of imports in the other files.
"""

#-------------------------------------------------------------------#

from tkinter import Tk, Frame, BOTH, Button, Entry, Label
from src.interface.widgets.entry_app import EntryApp
from src.interface.widgets.button_app import ButtonApp

#-------------------------------------------------------------------#

__all__ = ['Tk', 'Frame', 'BOTH', 'Button',
           'Entry', 'Label', 'EntryApp', 'ButtonApp']

"""
gui_utils.py

Defines the tkinter classes that are used in the application.
Helps to reduce the number of imports in the other files.
"""

#-------------------------------------------------------------------#

from tkinter import Tk, Frame, TOP, BOTTOM, BOTH, Button, Entry, Label, StringVar
from tkinter import Canvas, IntVar, Checkbutton, Menu, Text, Scrollbar, Radiobutton
from tkinter.ttk import Combobox
from tkcalendar import DateEntry
from src.interface.widgets.entry_app import EntryApp
from src.interface.widgets.button_app import ButtonApp
from src.interface.widgets.label_entry_pair import LabelEntryPair
from src.interface.widgets.add_serial import Serials

#-------------------------------------------------------------------#

__all__ = ['Tk', 'Frame', 'TOP', 'BOTTOM', 'BOTH', 'Button', 'IntVar',
           'Entry', 'Canvas', 'Label', 'EntryApp', 'ButtonApp', 'Checkbutton',
           'LabelEntryPair', 'Serials', 'Menu', 'Text', 'DateEntry', "Scrollbar",
           "Radiobutton", "Combobox", "StringVar"]

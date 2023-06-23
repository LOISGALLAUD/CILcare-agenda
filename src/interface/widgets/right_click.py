"""
right_click.py

This file contain the menu object displayed
next to the mouse when right clicking.
"""

#------------------------------------------------------------------------------#

from src.utils.graphical_utils import Menu

#------------------------------------------------------------------------------#

class RCMStudy(Menu):
    """
    Right Click Menu Study
    Frame displaying when right clicking
    on the study timeline.
    """
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager
        self.header_manager = self.manager.manager.manager.manager.header
        self.config(tearoff=False)
        self.add_command(label="Display", command=None)
        self.add_command(label="Modify",
                         command=self.header_manager.display_add_study)
        self.add_separator()
        self.add_command(label="Delete", command=None)

    def show(self, event):
        """
        Shows the menu at the given coordinates.
        """
        self.tk_popup(event.x_root, event.y_root)

class RCMSerial(Menu):
    """
    Right Click Menu Serial
    Frame displaying when right clicking
    on the serials.
    """
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager
        self.config(tearoff=False)
        self.add_command(label="Add a template", command=None)
        self.add_command(label="Add a task",
                         command=None)
        self.add_command(label="Activate", command=None)
        self.add_separator()
        self.add_command(label="Delete", command=None)

    def show(self, event):
        """
        Shows the menu at the given coordinates.
        """
        self.tk_popup(event.x_root, event.y_root)

class RCMTemplates(Menu):
    """
    Right Click Menu Templates
    Frame displaying when right clicking
    on the Templates.
    """
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager
        self.header_manager = self.manager.manager.manager.manager.header
        self.config(tearoff=False)
        self.add_command(label="Add a task",
                         command=self.header_manager.display_add_task)
        self.add_command(label="Modify", command=None)
        self.add_command(label="Display a task", command=None)
        self.add_separator()
        self.add_command(label="Delete", command=None)

    def show(self, event):
        """
        Shows the menu at the given coordinates.
        """
        self.tk_popup(event.x_root, event.y_root)

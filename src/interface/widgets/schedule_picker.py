"""
schedule_picker.py

Widget that allows the user to pick a schedule.
"""

#------------------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, Label, LabelEntryPair

#------------------------------------------------------------------------------#

class SchedulePicker(Frame):
    """
    Widget that allows the user to pick a schedule.
    """
    def __init__(self, manager:Frame):
        super().__init__(manager)
        self.manager = manager
        Label(self, text="Schedule", bg="#FFFFFF").pack(side='top', padx=10)

        # start hour
        start_hour_frame = Frame(self, bg="red")
        Label(start_hour_frame, text="Start hour", bg="#FFFFFF").pack(side='top', padx=10)
        hour_label = LabelEntryPair(start_hour_frame, "Hour")
        hour_label.pack(side='left', padx=5)
        minute_label = LabelEntryPair(start_hour_frame, "Minute")
        minute_label.pack(side='left', padx=5)

        # end hour
        end_hour_frame = Frame(self, bg="blue")
        Label(end_hour_frame, text="End hour", bg="#FFFFFF").pack(side='top', padx=10)
        hour_label = LabelEntryPair(end_hour_frame, "Hour")
        hour_label.pack(side='left', padx=5)
        minute_label = LabelEntryPair(end_hour_frame, "Minute")
        minute_label.pack(side='left', padx=5)
        start_hour_frame.pack(padx=10)
        end_hour_frame.pack(padx=10)

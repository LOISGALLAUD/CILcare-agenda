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
        Label(self, text="Schedule").pack(side='top')

        # start date
        start_date_frame = Frame(self)
        Label(start_date_frame, text="Start date", bg="#FFFFFF").pack(side='top')
        self.start_date_label = LabelEntryPair(start_date_frame, "date")
        self.start_date_label.pack(side='left',)

        # end date
        end_date_frame = Frame(self)
        Label(end_date_frame, text="End date", bg="#FFFFFF").pack(side='top')
        self.end_date_label = LabelEntryPair(end_date_frame, "date")
        self.end_date_label.pack(side='left')
        start_date_frame.pack()
        end_date_frame.pack()

    def get_start_date(self):
        """
        Returns the start date.
        """
        return self.start_date_label.entry.get()

    def get_end_date(self):
        """
        Returns the end date.
        """
        return self.end_date_label.entry.get()

    def get_schedule(self):
        """
        Returns the schedule.
        """
        return (self.get_start_date(), self.get_end_date())

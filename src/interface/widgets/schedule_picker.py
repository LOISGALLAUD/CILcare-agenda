"""
schedule_picker.py

Widget that allows the user to pick a schedule.
"""

#------------------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, Label, DateEntry, ButtonApp

#------------------------------------------------------------------------------#

def custom_drop_down(self):
    """Display or withdraw the drop-down calendar depending on its current state."""
    if self._calendar.winfo_ismapped():
        self._top_cal.withdraw()
    else:
        self._validate_date()
        date = self.parse_date(self.get())
        root_x = self.winfo_rootx()
        root_y = self.winfo_rooty() - 200 + self.winfo_height()
        if self.winfo_toplevel().attributes('-topmost'):
            self._top_cal.attributes('-topmost', True)
        else:
            self._top_cal.attributes('-topmost', False)
        self._top_cal.geometry('+%i+%i' % (root_x, root_y))
        self._top_cal.deiconify()
        self._calendar.focus_set()
        self._calendar.selection_set(date)

DateEntry.drop_down = custom_drop_down

class SchedulePicker(Frame):
    """
    Widget that allows the user to pick a schedule.
    """
    def __init__(self, manager:Frame):
        super().__init__(manager, bg="#494466", highlightbackground="#494466", highlightthickness=5)
        self.manager = manager
        Label(self, text="Schedule", bg="#494466",
              fg="white").pack(side='top',
                               fill="both", expand=True)

        picker_frame = Frame(self, bg="white")
        picker_frame.pack(side='left')

        # start date
        start_date_frame = Frame(picker_frame, bg="white")
        Label(start_date_frame, text="Start date", bg="#FFFFFF").pack(side='top')
        self.start_date_label = DateEntry(start_date_frame, width=20, background='#494466',
                                    foreground='white', borderwidth=2)
        self.start_date_label.pack(side='top')

        # end date
        end_date_frame = Frame(picker_frame, bg="white")
        Label(end_date_frame, text="End date", bg="#FFFFFF").pack(side='top')
        self.end_date_label = DateEntry(end_date_frame, width=20, background='#494466',
                                    foreground='white', borderwidth=2)
        self.end_date_label.pack(side='top')
        start_date_frame.pack(side='left')
        end_date_frame.pack(side='right')

        self.confirm_filtering_btn = ButtonApp(self, text="Confirm filters",
                                               custom_theme="Green",
                                                  command=None)
        self.confirm_filtering_btn.pack(side="right", fill="both", expand=True)

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

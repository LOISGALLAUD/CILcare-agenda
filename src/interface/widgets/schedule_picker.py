"""
schedule_picker.py

Widget that allows the user to pick a schedule.
"""
# pylint: disable=django-not-configured

# ------------------------------------------------------------------------------#

import datetime
from src.utils.graphical_utils import Frame, Label, DateEntry, ButtonApp

# ------------------------------------------------------------------------------#

# pylint: disable=protected-access


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

    def __init__(self, manager: Frame):
        super().__init__(manager, bg="#494466")
        self.manager = manager
        Label(self, text="Schedule", bg="#494466",
              fg="white").pack(side='top',
                               fill="both", expand=True)

        picker_frame = Frame(self, bg="white")
        picker_frame.pack(side='left')

        # start date
        start_date_frame = Frame(picker_frame, bg="white")
        Label(start_date_frame, text="Start date",
              bg="#FFFFFF").pack(side='top')
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

        self.confirm_filtering_btn = ButtonApp(self, text="Update schedule",
                                               custom_theme="Green",
                                               command=self.confirm_filtering)
        self.confirm_filtering_btn.pack(side="right", fill="both", expand=True)
        self.get_schedule()

    def get_start_date(self):
        """
        Returns the start date.
        """
        return self.start_date_label.get()

    def get_end_date(self):
        """
        Returns the end date.
        """
        return self.end_date_label.get()

    def get_schedule(self):
        """
        Returns in a tuple the start date and the end date.
        Verify that the start date is before the end date and
        that the dates are not separated by more than a month.
        """
        start_date_str = self.get_start_date()
        end_date_str = self.get_end_date()
        start_date = datetime.datetime.strptime(start_date_str, "%d/%m/%Y")
        end_date = datetime.datetime.strptime(end_date_str, "%d/%m/%Y")

        if start_date > end_date:
            start_date, end_date = end_date, start_date

        if (end_date - start_date) > datetime.timedelta(days=30):
            end_date = start_date + datetime.timedelta(days=30)

        return start_date, end_date

    def confirm_filtering(self):
        """
        Set the command to execute when the user confirms the filtering.
        """
        start_date, end_date = self.get_schedule()
        time_interval = end_date - start_date
        day_of_week = start_date.strftime("%A")

        if not time_interval.days:
            return
        time_interval = time_interval.days*24+1  # in hours

        if time_interval >= 3*24+1:
            self.manager.manager.body.studies_template.update_timelines(
                start_date, time_interval)
        else:
            self.manager.manager.body.studies_template.update_timelines(
                start_date, time_interval, day_of_week)

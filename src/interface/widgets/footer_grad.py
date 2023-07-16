"""
footer_graduation.py

Canvas in which is drawn the time graduation.
"""

# -------------------------------------------------------------------#

from datetime import datetime
from src.utils.graphical_utils import Frame, Canvas, Label, Scrollbar

# -------------------------------------------------------------------#


class FooterFrame(Frame):
    """
    Frame containing the footer.
    """

    def __init__(self, master, study_timeline, daysoff_timeline, day_of_week=None, **kwargs):
        super().__init__(master, bg='#494466', **kwargs)
        self.master = master
        self.study_timeline = study_timeline
        self.daysoff_timeline = daysoff_timeline
        self.coeff_config = self.master.time_interval//24
        self.start_weekday = day_of_week
        self.grid(row=3, column=0, sticky='nsew')
        self.propagate(False)
        self.config(height=70)

        self.scrollbar = Scrollbar(self, orient="horizontal",
                                   width=20)
        self.scrollbar.pack(side="bottom", fill="x")
        self.canvas = Canvas(
            self, xscrollcommand=self.scrollbar.set, bg='white',)
        self.canvas.pack(fill="both", expand=True, side="top")
        self.scrollbar.config(command=self.h_scroll)

        self.inner_frame = Frame(self.canvas, border=0,
                                 borderwidth=0, highlightthickness=0)
        self.update_idletasks()

        self.window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw',
                                                width=self.get_correct_width(self.master.time_interval))

        self.canvas.bind('<Configure>', lambda event: self.canvas.configure
                         (scrollregion=self.canvas.bbox('all')))

        self.graduation_frame = GraduationFrame(self, self.inner_frame)

    def h_scroll(self, *args):
        """
        Simultaneous horizontal scroll of the two timelines.
        """
        self.study_timeline.canvas.xview(*args)
        self.daysoff_timeline.canvas.xview(*args)
        self.canvas.xview(*args)

    def get_correct_width(self, time_interval):
        """
        Return a pertinent width for the canvas knowing the time
        interval, the starting time and the width of the window.
        """
        x_step = self.master.winfo_width() / 25
        return time_interval * x_step


class GraduationFrame(Frame):
    """
    Frame container of the time graduation.
    """

    def __init__(self, master, scrollable_frame, **kwargs):
        super().__init__(master=scrollable_frame, **kwargs)
        self.master = master
        self.pack(fill='x',)
        self.config(height=500)
        self.update_idletasks()

        self.time_frame = TimeFrame(self)


class TimeFrame(Frame):
    """
    Frame containing the time.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1, uniform='group')
        self.grid_columnconfigure(1, weight=12*self.master.master.coeff_config,
                                  uniform='group')
        Label(self, text="TEMPS", bg="#494466", fg="white",
              wraplength=150).grid(row=0, column=0, sticky='nsew')

        self.pack(fill='x')
        self.update_idletasks()

        unity_container = Frame(self)
        unity_container.grid(row=0, column=1, sticky='nsew')
        self.unity_frame = UnityFrame(unity_container)


class UnityFrame(Frame):
    """
    Frame containing the unity of time.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1, uniform='group')
        self.grid_columnconfigure(1, weight=13*self.master.master.master.master.coeff_config,
                                  uniform='group')
        Label(self, text="UNITE DE TEMPS", bg="#d3ccff", fg="black",
              wraplength=150).grid(row=0, column=0, sticky='nsew')

        self.pack(fill='x')
        self.update_idletasks()
        self.config(height=50)
        self.time_canvas = TimeCanvas(self)


class TimeCanvas(Canvas):
    """
    Canvas containing the time.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, bg="white", height=50,
                         **kwargs)
        self.grid(row=0, column=1, sticky='ew')
        self.master = master

        self.width = 0
        self.height = 0
        self.time_interval = 0
        self.x_step = 0
        self.starting_time = 0

        self.update_idletasks()
        self.get_time_graduations()
        self.create_timeline(
            self.master.master.master.master.master.master.time_interval, 0)

    def get_time_graduations(self) -> list:
        """
        Get the time graduations.
        """
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.time_interval = self.master.master.master.master.master.master.time_interval
        self.x_step = self.width / self.time_interval
        self.starting_time = self.master.master.master.master.master.master.starting_time

    def create_timeline(self, time_interval: int, start_time: int, _day_of_week: str = None):
        """
        Creates the timeline.
        """
        width = self.winfo_width()
        height = self.winfo_height()
        x_step = width / time_interval
        start_time = 0
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        if _day_of_week is None:
            _day_of_week = datetime.now().strftime("%A")

        # Determine the start day index
        start_day_index = days.index(
            _day_of_week[:3])

        # Draw the timeline
        for i in range(time_interval+1):
            x_pos = i * x_step
            self.create_line(x_pos, 0, x_pos, height,
                             fill='#d9d9d9', tags="timeline")
            time_label = start_time + i

            # Calculate the current day
            current_day_index = (start_day_index + (time_label // 24)) % 7
            current_day = days[current_day_index]

            # Display the time label and day of the week
            if time_label % 24 == 0:
                self.create_text(x_pos + x_step / 4, 20,
                                 text=current_day,
                                 anchor='n', fill='black', tags="timescale")
            else:
                self.create_text(x_pos + x_step / 4, 20,
                                 text=str(time_label % 24) + "h",
                                 anchor='n', fill='grey', tags="timescale")

    def update_timeline(self, start_date, time_interval, day_of_week) -> None:
        """
        Update the timeline.
        """
        self.delete('timeline')
        self.delete('timescale')
        self.create_timeline(time_interval, start_date, day_of_week)

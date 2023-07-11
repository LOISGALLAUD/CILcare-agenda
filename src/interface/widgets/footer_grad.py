"""
footer_graduation.py

Canvas in which is drawn the time graduation.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, Canvas, Label, Scrollbar

#-------------------------------------------------------------------#

class FooterFrame(Frame):
    """
    Frame containing the footer.
    """
    def __init__(self, master, frame_to_scroll:list, **kwargs):
        super().__init__(master, bg='#494466', **kwargs)
        self.master = master
        self.coeff_config = 80//24
        self.pack(fill='both', side='bottom', expand=True)
        self.propagate(False)
        self.config(height=70)
        self.update_idletasks()

        scrollbar = Scrollbar(self, orient="horizontal",
                              width=20)
        scrollbar.pack(side="bottom", fill="x")
        self.canvas = Canvas(self, xscrollcommand=scrollbar.set, bg='purple',)
        self.canvas.pack(fill="both", expand=True, side="top")
        scrollbar.config(command=self.canvas.xview)

        inner_frame = Frame(self.canvas, border=0,
                            borderwidth=0, highlightthickness=0)
        self.update_idletasks()

        self.canvas.create_window((0, 0), window=inner_frame, anchor='w',
                             width=self.get_correct_width())
        self.canvas.bind('<Configure>', lambda event:self.canvas.configure
                    (scrollregion=self.canvas.bbox('all')))
        self.graduation_frame = GraduationFrame(self, inner_frame)
        self.graduation_frame.bind('<Configure>',
                        lambda event: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        for frame in frame_to_scroll:
            scrollbar.config(command=frame.canvas.xview)

    def get_correct_width(self):
        """
        Return a pertinent width for the canvas knowing the time
        interval, the starting time and the width of the window.
        """
        x_step = self.winfo_width() / 25
        return 80 * x_step

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
        Label(self, text="UNITE DE TEMPS", bg="#494466", fg="white",
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
        self.create_timeline(80, 0)

    def get_time_graduations(self) -> list:
        """
        Get the time graduations.
        """
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.time_interval = self.master.master.master.master.master.master.time_interval
        self.x_step = self.width / self.time_interval
        self.starting_time = self.master.master.master.master.master.master.starting_time

    def create_timeline(self, time_interval:int, start_time:int):
        """
        Creates the timeline.
        """
        width = self.winfo_width()
        height = self.winfo_height()
        x_step = width / time_interval

        # Draw the timeline
        for i in range(time_interval):
            x_pos = i * x_step
            self.create_line(x_pos, 0, x_pos, height, fill='#d9d9d9')
            time_label = start_time + i
            self.create_text(x_pos + x_step / 4, 20,
                                text=str(time_label) + "h",
                                anchor='n', fill='grey', tags="timeline")

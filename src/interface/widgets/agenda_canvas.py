"""
agenda_canvas.py

Describe the agenda canvas in the add days off menu.
It contains visual representation of the disponibilities
of operators.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, Canvas, Label, Scrollbar

#-------------------------------------------------------------------#

class WorkingFrame(Frame):
    """
    Represents the working frame.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="black", **kwargs)
        self.master = master
        self.coeff_config = self.master.time_interval//24
        self.pack(fill='both', expand=True, side='bottom', pady=(0, 10))
        self.update_idletasks()

        self.serial_canvases = []

        scrollbar = Scrollbar(self, orient="vertical", width=20)
        scrollbar.pack(side="right", fill="y")
        self.canvas = Canvas(self, yscrollcommand=scrollbar.set)
        self.canvas.pack(side="top", fill="both", expand=True)
        scrollbar.config(command=self.canvas.yview)
        self.inner_frame = Frame(self.canvas, border=0, borderwidth=0, highlightthickness=0)
        self.update_idletasks()
        self.canvas.create_window((0, 0), window=self.inner_frame,
                                  anchor='nw', width=self.get_correct_width())
        self.canvas.bind('<Configure>',
                    lambda event: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        self.agenda_frame = AgendaFrame(self, self.inner_frame)
        self.agenda_frame.bind('<Configure>',
                        lambda event: self.canvas.configure(scrollregion=self.canvas.bbox('all')))


    def create_timeline(self, canvas, time_interval):
        """
        Creates the timeline.
        """
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        x_step = width / time_interval

        # Draw the timeline
        for i in range(time_interval):
            x_pos = i * x_step
            canvas.create_line(x_pos, 0, x_pos, height, fill='#d9d9d9')

    def get_correct_width(self):
        """
        Return a pertinent width for the canvas knowing the time
        interval, the starting time and the width of the window.
        """
        x_step = self.master.winfo_width() / 25
        return self.master.time_interval * x_step

    def add_study(self, study_name) -> None:
        """
        Adds a study to the timeline.
        """
        return StudyFrame(self.agenda_frame, study_name)

    def add_serial(self, study_frame, serial_name) -> None:
        """
        Adds a serial to the timeline.
        """
        serial_frame = SerialFrame(study_frame.serial_container, serial_name)
        self.serial_canvases.append(serial_frame.serial_canvas)
        return serial_frame

    def add_task(self, serial_frame) -> None:
        """
        Adds a task to the timeline.
        """
        TaskRectangle(serial_frame.serial_canvas, 'Task name', 8, 12)


class AgendaFrame(Frame):
    """
    Agenda canvas with scrolling.
    """
    def __init__(self, master, scrollable_frame, **kwargs):
        super().__init__(master=scrollable_frame, **kwargs)
        self.master = master
        self.pack(fill='x')
        self.update_idletasks()

class StudyFrame(Frame):
    """
    Frame containing a study and its serials.
    """
    def __init__(self, master, name, **kwargs):
        super().__init__(master, bg="white", **kwargs)
        self.coeff_config = master.master.coeff_config
        self.grid_columnconfigure(0, weight=1, uniform='group')
        self.grid_columnconfigure(1, weight=12*self.coeff_config, uniform='group')

        Label(self, text=name, bg="#494466", fg="white",
              wraplength=150).grid(row=0, column=0, sticky='nsew')

        self.serial_container = Frame(self)
        self.serial_container.grid(row=0, column=1, sticky='ew')

        self.pack(fill="x")
        self.update_idletasks()

class SerialFrame(Frame):
    """
    Frame containing a serial and its tasks.
    """
    def __init__(self, master, name, **kwargs):
        super().__init__(master, bg='white', **kwargs)
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, uniform='group')
        self.grid_columnconfigure(1, weight=13*self.master.master.coeff_config, uniform='group')

        Label(self, text=name, fg="black", bg='#d3ccff',
              wraplength=150).grid(row=0, column=0, sticky='nsew', pady=5)

        self.pack(fill="x")
        self.update_idletasks()
        self.config(height=50)
        self.serial_canvas = SerialCanvas(self)

class SerialCanvas(Canvas):
    """
    Canvas containing the tasks of a serial.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="white", **kwargs)
        self.grid(row=0, column=1, sticky='ew')
        self.master = master

        self.width = 0
        self.height = 0
        self.time_interval = 0
        self.x_step = 0
        self.starting_time = 0

        self.selected_rectangles = []  # List of selected rectangles

        self.update_idletasks()
        self.get_time_graduations()
        self.master.master.master.master.master.create_timeline(
            self, self.time_interval)
        self.bind('<Button-1>', self.deselect_rectangles)

        self.bind('<Enter>', self.bind_mousewheel)
        self.bind('<Leave>', self.unbind_mousewheel)

    def bind_mousewheel(self, _event):
        """
        Bind mousewheel to the canvas.
        """
        self.bind('<Button-4>', self.on_scroll_up)
        self.bind('<Button-5>', self.on_scroll_down)

    def unbind_mousewheel(self, _event):
        """
        Unbind mousewheel to the canvas.
        """
        self.unbind('<Button-4>')
        self.unbind('<Button-5>')

    def on_scroll_up(self, _event):
        """
        Scroll up.
        """
        self.master.master.master.master.master.canvas.yview_scroll(-1, 'units')

    def on_scroll_down(self, _event):
        """
        Scroll down.
        """
        self.master.master.master.master.master.canvas.yview_scroll(1, 'units')

    def get_time_graduations(self) -> list:
        """
        Get the time graduations.
        """
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.time_interval = self.master.master.master.master.master.master.time_interval
        self.x_step = self.width / self.time_interval
        self.starting_time = self.master.master.master.master.master.master.starting_time

    def deselect_rectangles(self, _event) -> None:
        """
        Deselect all rectangles when clicking on the canvas.
        """
        item = self.find_withtag('current')  # Récupérer l'élément sur lequel le clic a eu lieu
        if len(item) == 1 and self.type(item) == 'rectangle':
            return  # Ne rien faire si le clic a eu lieu sur un rectangle
        if len(item) == 1 and self.type(item) == 'text':
            return # Ne rien faire si le clic a eu lieu sur un texte

        for rect in self.selected_rectangles:
            self.itemconfig(rect.rect, fill='#494466')
        self.selected_rectangles.clear()

    def update_timeline(self) -> None:
        """
        Update the timeline.
        """
        self.delete('timeline')
        self.master.master.master.master.master.create_timeline(
            self, self.time_interval, self.starting_time, 1)

class TaskRectangle:
    """
    Represents a task on the canvas.
    """
    height = 40
    def __init__(self, canvas_manager: Canvas, name: str,
                 starting_hour: int, ending_hour:int) -> None:
        self.canvas_manager = canvas_manager
        self.start_x_pos = 0  # Position de départ du rectangle
        self.start_y_pos = 0  # Position de départ du rectangle
        self.is_dragging = False  # Indicateur de déplacement en cours

        self.name = name
        self.x_pos = self.get_x_pos(starting_hour)
        self.width = self.get_x_pos(ending_hour) - self.x_pos
        self.y_pos = 5

        self.draw_task()

    def get_x_pos(self, starting_hour: int) -> int:
        """
        Convert the starting hour to the x position on the canvas.
        """
        return starting_hour * self.canvas_manager.x_step

    def draw_task(self) -> None:
        """
        Draws the task on the canvas.
        """
        self.rect = self.canvas_manager.create_rectangle(self.x_pos, self.y_pos,
                                                    self.x_pos + self.width,
                                                    self.y_pos + self.height, fill='#494466')
        self.text = self.canvas_manager.create_text(self.x_pos + self.width / 2,
                                                    self.y_pos + self.height / 2,
                                                    text=self.name,
                                                    fill='white')
        self.canvas_manager.tag_bind(self.rect, '<ButtonPress-1>', self.on_click)
        self.canvas_manager.tag_bind(self.rect, '<B1-Motion>', self.on_drag)
        self.canvas_manager.tag_bind(self.text, '<ButtonPress-1>', self.on_click)
        self.canvas_manager.tag_bind(self.text, '<B1-Motion>', self.on_drag)

    def on_click(self, event) -> None:
        """
        Event handler for clicking on the rectangle.
        """
        if event.state & 4:  # 4 corresponds to the Ctrl key
            # Toggle selection
            if self in self.canvas_manager.selected_rectangles:
                self.canvas_manager.selected_rectangles.remove(self)
                self.canvas_manager.itemconfig(self.rect, fill='#494466')
            else:
                self.canvas_manager.selected_rectangles.append(self)
                self.canvas_manager.itemconfig(self.rect, fill='#a499e5')
        else:
            if self not in self.canvas_manager.selected_rectangles:
                # Deselect all rectangles
                for rect in self.canvas_manager.selected_rectangles:
                    self.canvas_manager.itemconfig(rect.rect, fill='#494466')
                self.canvas_manager.selected_rectangles.clear()

                # Select the current rectangle
                self.canvas_manager.selected_rectangles.append(self)
                self.canvas_manager.itemconfig(self.rect, fill='#a499e5')

        self.start_x_pos = event.x
        self.start_y_pos = event.y

    def on_drag(self, event) -> None:
        """
        Event handler for dragging the rectangle.
        """
        for rect in self.canvas_manager.selected_rectangles:
            if rect.is_dragging:
                continue
            rect.is_dragging = True

        if not self.is_dragging:
            self.is_dragging = True
            # Deselect other rectangles except the current one
            for rect in self.canvas_manager.selected_rectangles:
                if rect != self:
                    self.canvas_manager.itemconfig(rect.rect, fill='#494466')
            self.canvas_manager.selected_rectangles = [self]
            self.canvas_manager.itemconfig(self.rect, fill=' "a499e5')

        dx_pos = event.x - self.start_x_pos

        for rect in self.canvas_manager.selected_rectangles:
            # Move the rectangle with the step on the X axis within a range
            if abs(dx_pos) >= rect.canvas_manager.x_step:
                steps = int(dx_pos / rect.canvas_manager.x_step)
                dx_pos = steps * rect.canvas_manager.x_step
                rect.canvas_manager.move(rect.rect, dx_pos, 0)
                rect.start_x_pos = event.x

            # Move the text
            x1, y1, x2, y2 = rect.canvas_manager.coords(rect.rect)
            text_x = (x1 + x2) / 2
            text_y = (y1 + y2) / 2
            rect.canvas_manager.coords(rect.text, text_x, text_y)

        self.is_dragging = False

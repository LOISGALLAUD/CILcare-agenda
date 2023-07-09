"""
task_rectangle.py

Contains the TaskRectangle class, which is a rectangle that represents a task on the canvas.
"""

#------------------------------------------------------------------------------#

from src.utils.graphical_utils import Canvas

#------------------------------------------------------------------------------#

class TaskRectangle:
    """
    Represents a task on the canvas.
    """
    height = 40
    def __init__(self, canvas_manager: Canvas, name: str,
                 starting_hour: int, ending_hour:int) -> None:
        self.canvas_manager = canvas_manager
        self.is_dragging = False  # Indicateur de déplacement en cours

        self.name = name
        self.x_pos = self.get_x_pos(starting_hour)
        self.width = self.get_x_pos(ending_hour) - self.x_pos
        self.y_pos = self.canvas_manager.height / 2 # arbitrary constant

        self.start_x_pos, self.start_y_pos = None, None
        self.rect = None
        self.text = None

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
                                                    self.y_pos + self.height, fill='darkred')
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
                self.canvas_manager.itemconfig(self.rect, fill='darkred')
            else:
                self.canvas_manager.selected_rectangles.append(self)
                self.canvas_manager.itemconfig(self.rect, fill='red')
        else:
            if self not in self.canvas_manager.selected_rectangles:
                # Deselect all rectangles
                for rect in self.canvas_manager.selected_rectangles:
                    self.canvas_manager.itemconfig(rect.rect, fill='darkred')
                self.canvas_manager.selected_rectangles.clear()

                # Select the current rectangle
                self.canvas_manager.selected_rectangles.append(self)
                self.canvas_manager.itemconfig(self.rect, fill='red')

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
                    self.canvas_manager.itemconfig(rect.rect, fill='darkred')
            self.canvas_manager.selected_rectangles = [self]
            self.canvas_manager.itemconfig(self.rect, fill='red')

        dx_pos = event.x - self.start_x_pos
        dy_pos = event.y - self.start_y_pos

        for rect in self.canvas_manager.selected_rectangles:
            # Move the rectangle with the step on the X axis within a range
            if abs(dx_pos) >= rect.canvas_manager.x_step:
                steps = int(dx_pos / rect.canvas_manager.x_step)
                dx_pos = steps * rect.canvas_manager.x_step
                rect.canvas_manager.move(rect.rect, dx_pos, 0)
                rect.start_x_pos = event.x

            # Move the rectangle on the Y axis
            rect.canvas_manager.move(rect.rect, 0, dy_pos)
            rect.start_y_pos = event.y

            # Move the text
            x1, y1, x2, y2 = rect.canvas_manager.coords(rect.rect)
            text_x = (x1 + x2) / 2
            text_y = (y1 + y2) / 2
            rect.canvas_manager.coords(rect.text, text_x, text_y)

        self.is_dragging = False

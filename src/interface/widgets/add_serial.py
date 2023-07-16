"""
add_serial.py

Add serial template.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, LabelEntryPair, Label, ButtonApp

#-------------------------------------------------------------------#

class Serials(Frame):
    """
    Unsorted serials of the study.
    The user can add as many serials as he wants.
    Scrollable frame.
    """
    parameters = ["Name", "Number", "Ears"]
    MAX_SERIALS = 10
    def __init__(self, study_template) -> None:
        super().__init__(study_template)
        self.configure(bg="#FFFFFF")
        self.manager = study_template
        self.displayed_serial = 0
        self.name=None
        self.number=None
        self.ears=None
        Label(self, text="Serials: ", bg="#FFFFFF",
              fg="#000000").pack(fill='both', side='left', pady=10)
        ButtonApp(self, text="+", bg="#FFFFFF",
                  command=self.add_serial_line).pack(fill='both', side='left', pady=10)

    def add_serial_line(self) -> None:
        """
        Add a line to the serial widget
        """
        if self.displayed_serial >= self.MAX_SERIALS:
            return
        line_frame = Frame(self, bg="white")
        line_frame.pack(fill='both', side='top')

        self.name = LabelEntryPair(line_frame, "Name")
        self.name.pack(fill='both', side='left')

        self.number = LabelEntryPair(line_frame, "Number")
        self.number.pack(fill='both', side='left')

        self.ears = LabelEntryPair(line_frame, "Ears")
        self.ears.pack(fill='both', side='left')

        ButtonApp(line_frame, text="X", bg="#FFFFFF",
                    command=lambda: self.remove_serial_line(line_frame)).pack(fill='both',
                                                                              side='left')
        self.displayed_serial += 1

    def remove_serial_line(self, line_frame) -> None:
        """
        Remove a line from the serial widget
        """
        self.displayed_serial -= 1
        line_frame.destroy()

    def get_data(self) -> dict:
        """
        Get the data from the serial widget
        """
        data = []
        for line in self.winfo_children():
            if isinstance(line, Frame):
                serial = {}
                for entry in line.winfo_children():
                    if isinstance(entry, LabelEntryPair):
                        serial[entry.label.cget("text")[:-1].lower()] = entry.entry.get()
                data.append(serial)
        return data

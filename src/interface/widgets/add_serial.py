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
    def __init__(self, study_template) -> None:
        super().__init__(study_template)
        self.manager = study_template
        self.configure(bg="#888888")
        Label(self, text="Serials: ", bg="#FFFFFF",
              fg="#000000").pack(fill='both', side='left', pady=10)
        ButtonApp(self, text="+", bg="#FFFFFF",
                  command=self.add_serial_line).pack(fill='both', side='left', pady=10)

    def add_serial_line(self) -> None:
        """
        Add a line to the serial widget
        """
        line_frame = Frame(self, bg="#4440ae")
        line_frame.pack(fill='both', side='top', pady=10)
        for parameter in self.parameters:
            LabelEntryPair(line_frame, parameter).pack(fill='both', side='left', padx=10, pady=10)

        ButtonApp(line_frame, text="X", bg="#FFFFFF",
                    command=lambda: self.remove_serial_line(line_frame)).pack(fill='both', side='left', padx=10, pady=10)

    def remove_serial_line(self, line_frame) -> None:
        """
        Remove a line from the serial widget
        """
        line_frame.destroy()

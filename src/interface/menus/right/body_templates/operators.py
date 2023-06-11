"""
operators.py

Contains the operators page.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, Label, Canvas

#-------------------------------------------------------------------#

class OperatorsTemplate(Frame):
    """
    Contains the Frame in which will be displayed every
    templates related to the studies.
    """
    operators_examples = ["Operator 1", "Operator 2", "Operator 3"]
    def __init__(self, body=None):
        super().__init__(body)
        self.manager = body
        self.configure(bg="gold")
        self.propagate(False)

        self.setup_lines()

    def setup_lines(self) -> None:
        """
        Setup the lines of the operators page.
        Contains operators names on the left
        and their disponibilities on the right.
        """

        for operators in self.operators_examples:
            line_frame = Frame(self, bg="blue")
            line_frame.propagate(False)
            line_frame.rowconfigure(0, weight=1)
            line_frame.columnconfigure(0, weight=1)
            line_frame.columnconfigure(1, weight=4)
            line_frame.pack(fill="both", expand=True, side="top")
            Label(line_frame, text=operators).pack(side="left", fill="both")
            Canvas(line_frame, width=100,  height=100, bg="red").pack(side="right",
                                                                      fill="both",
                                                                      expand=True)

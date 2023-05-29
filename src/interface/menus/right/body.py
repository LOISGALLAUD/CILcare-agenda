"""
body.py

Configure MarcoNeo's body on its shopping menu.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame
from src.interface.menus.right.body_templates.studies import StudiesTemplate

#-------------------------------------------------------------------#

class Body(Frame):
    """
    Contains the items to be displayed in the shopping page.
    """
    def __init__(self, right_grid=None):
        super().__init__(right_grid)
        self.manager = right_grid
        self.configure(bg="purple")
        self.width = None
        self.height = None
        self.studies_template = None
        self.setup_studies()

    def setup_studies(self) -> None:
        """
        Setup the studies page.
        """
        self.studies_template = StudiesTemplate(self)
        self.studies_template.pack(fill='both', expand=True, side='top', padx=10, pady=10)

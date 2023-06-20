"""
body.py

Configure MarcoNeo's body on its shopping menu.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame
from src.interface.menus.right.body_templates.studies import StudiesTemplate
from src.interface.menus.right.body_templates.operators import OperatorsTemplate
from src.interface.menus.right.body_templates.rooms import RoomsTemplate
from src.interface.menus.right.body_templates.equipment import EquipmentTemplate
from src.interface.menus.right.body_templates.qualifications import QualificationTemplate
from src.interface.menus.right.body_templates.animal_types import AnimalTypeTemplate

#-------------------------------------------------------------------#

class Body(Frame):
    """
    Contains the items to be displayed in the shopping page.
    """
    def __init__(self, right_grid=None):
        super().__init__(right_grid)
        self.manager = right_grid
        self.width = None
        self.height = None
        self.studies_template = None
        self.operators_template = None
        self.rooms_template = None
        self.equipment_template = None
        self.qualification_template = None
        self.animal_types_template = None

        self.setup_studies()

    def setup_studies(self) -> None:
        """
        Setup the studies page
        """
        self.studies_template = StudiesTemplate(self)
        self.studies_template.pack(fill='both', expand=True, side='top')

    def setup_operators(self) -> None:
        """
        Setup the operators page.
        """
        self.operators_template = OperatorsTemplate(self)
        self.operators_template.pack(fill='both', expand=True, side='top')

    def setup_rooms(self):
        """
        Setup the rooms page.
        """
        self.rooms_template = RoomsTemplate(self)
        self.rooms_template.pack(fill='both', expand=True, side='top')

    def setup_equipment(self):
        """
        Setup the equipment page.
        """
        self.equipment_template = EquipmentTemplate(self)
        self.equipment_template.pack(fill='both', expand=True, side='top')

    def setup_qualification(self):
        """
        Setup the qualification page.
        """
        self.qualification_template = QualificationTemplate(self)
        self.qualification_template.pack(fill='both', expand=True, side='top')

    def setup_animal_types(self):
        """
        Setup the animal_type page.
        """
        self.animal_types_template = AnimalTypeTemplate(self)
        self.animal_types_template.pack(fill='both', expand=True, side='top')

    def update_body(self, toggle):
        """
        Updates the items displayed in the body.
        """
        self.clear_body()
        match toggle:
            case "Studies":
                self.setup_studies()
            case "Operators":
                self.setup_operators()
            case "Rooms":
                self.setup_rooms()
            case "Equipment":
                self.setup_equipment()
            case "Qualifications":
                self.setup_qualification()
            case "Animal types":
                self.setup_animal_types()
            case _:
                print("Error: Invalid toggle.")

    def clear_body(self):
        """
        Clears the body.
        """
        for child in self.winfo_children():
            child.destroy()

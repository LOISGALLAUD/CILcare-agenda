"""
header.py

Top section of the shopping menu.
"""

#-------------------------------------------------------------------#

from src.utils.graphical_utils import Frame, ButtonApp

#-------------------------------------------------------------------#


class Header(Frame):
    """
    Top section of the shopping menu.
    """
    def __init__(self, manager=None) -> None:
        super().__init__(manager)
        self.manager = manager
        # Default toggle
        self.current_toggle = None
        self.propagate(False)
        self.configure(bg="#2bb5a6")

        self.add_study_btn = None
        self.add_days_off_btn = None
        self.add_operator_btn = None
        self.add_room_btn = None
        self.add_equipment_btn = None
        self.add_qualification_btn = None
        self.add_animal_types_btn = None
        self.add_templates_btn = None

        self.setup_widgets_studies()

    def setup_widgets_studies(self) -> bool:
        """
        Setup the widgets of the header.
        """
        self.add_study_btn = ButtonApp(self, "Green", text="Add study",
                                       command=self.display_add_study)
        self.add_days_off_btn = ButtonApp(self, "Green", text="Add days off",
                                            command=self.display_add_days_off)

        self.add_study_btn.pack(side="left", fill="x", expand=True,
                                padx=10, pady=10)
        self.add_days_off_btn.pack(side="left", fill="x", expand=True,
                                   padx=10, pady=10)
        return True

    def setup_widgets_operators(self) -> bool:
        """
        Setup the widgets of the header.
        """
        self.add_operator_btn = ButtonApp(self, "Green", text="Add operator",
                                          command=self.display_add_operator)
        self.add_operator_btn.pack(side="left",
                                   fill="x",expand=True,
                                   padx=10, pady=10)
        return True

    def setup_widgets_rooms(self) -> bool:
        """
        Setup the widgets of the header.
        """
        self.add_room_btn = ButtonApp(self, "Green", text="Add room",
                                      command=self.display_add_room)
        self.add_room_btn.pack(side="left",
                               fill="x",expand=True,
                               padx=10, pady=10)
        return True

    def setup_widgets_equipments(self) -> bool:
        """
        Setup the widgets of the header.
        """
        self.add_equipment_btn = ButtonApp(self, "Green", text="Add equipment",
                                      command=self.display_add_equipment)
        self.add_equipment_btn.pack(side="left",
                               fill="x",expand=True,
                               padx=10, pady=10)
        return True

    def setup_widgets_qualifications(self) -> bool:
        """
        Setup the widgets of the header.
        """
        self.add_qualification_btn = ButtonApp(self, "Green", text="Add qualification",
                                      command=self.display_add_qualification)
        self.add_qualification_btn.pack(side="left",
                               fill="x",expand=True,
                               padx=10, pady=10)
        return True

    def setup_widgets_animal_types(self) -> bool:
        """
        Setup the widgets of the header.
        """
        self.add_animal_types_btn = ButtonApp(self, "Green", text="Add an animal type",
                                      command=self.display_add_animal_types)
        self.add_animal_types_btn.pack(side="left",
                               fill="x",expand=True,
                               padx=10, pady=10)
        return True

    def setup_widgets_templates(self) -> bool:
        """
        Setup the widgets of the header.
        """
        self.add_templates_btn = ButtonApp(self, "Green", text="Add a template",
                                      command=self.display_add_templates)
        self.add_templates_btn.pack(side="left",
                               fill="x",expand=True,
                               padx=10, pady=10)
        return True

    def reset_modifications(self) -> None:
        """
        Resets the modifications made by the user.
        """
        self.add_days_off_btn.config(state="normal")
        self.add_study_btn.config(state="normal")

    def display_add_study(self) -> None:
        """
        Displays the add study template.
        """
        self.add_days_off_btn.config(state="disabled")
        self.manager.body.studies_template.setup_add_study()

    def display_add_days_off(self) -> None:
        """
        Displays the add days off template.
        """
        self.add_study_btn.config(state="disabled")
        self.manager.body.studies_template.setup_add_days_off()

    def display_add_operator(self) -> None:
        """
        Displays the add operator template.
        """
        self.manager.body.operators_template.from_timeline_to_add_operators()

    def display_add_room(self) -> None:
        """
        Displays the add room template.
        """
        self.manager.body.rooms_template.from_timeline_to_add_room()

    def display_add_equipment(self) -> None:
        """
        Displays the add equipments template.
        """
        self.manager.body.equipment_template.from_timeline_to_add_equipments()

    def display_add_qualification(self) -> None:
        """
        Displays the add qualifications template.
        """
        self.manager.body.qualification_template.from_timeline_to_add_qualifications()

    def display_add_animal_types(self) -> None:
        """
        Displays the add animal_types template.
        """
        self.manager.body.animal_types_template.from_timeline_to_add_animal_types()

    def display_add_templates(self) -> None:
        """
        Displays the add templates template.
        """
        self.manager.body.templates_template.from_timeline_to_add_templates()

    def display_add_task(self) -> None:
        """
        Displays the add task template.
        """
        self.manager.body.templates_template.from_timeline_to_add_tasks()

    def update_header(self, toggle):
        """
        Updates the header.
        """
        self.clear_header()
        match toggle:
            case "Studies":
                self.setup_widgets_studies()
            case "Operators":
                self.setup_widgets_operators()
            case "Rooms":
                self.setup_widgets_rooms()
            case "Equipment":
                self.setup_widgets_equipments()
            case "Qualifications":
                self.setup_widgets_qualifications()
            case "Animal types":
                self.setup_widgets_animal_types()
            case "Templates":
                self.setup_widgets_templates()
            case _:
                self.manager.gui.loggers.log.error("No toggle match found")
                print("Error: No match found")

    def clear_header(self):
        """
        Clears the header.
        """
        for widget in self.winfo_children():
            widget.destroy()

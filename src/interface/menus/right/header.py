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
        print("Displaying add operator template.")
        return
        self.manager.body.operators_template.setup_add_operator()

    def update_header(self, toggle):
        """
        Updates the header.
        """
        self.clear_header()
        print(f"Updating header with {toggle}.")
        match toggle:
            case "Studies":
                self.setup_widgets_studies()
            case "Operators":
                self.setup_widgets_operators()

    def clear_header(self):
        """
        Clears the header.
        """
        for widget in self.winfo_children():
            widget.destroy()

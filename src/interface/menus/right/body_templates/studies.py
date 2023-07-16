"""
studies.py

Studies template for the body
"""

# -------------------------------------------------------------------#

# from datetime import datetime
from tkcolorpicker import askcolor
from src.utils.graphical_utils import Frame, Canvas, Label, ButtonApp, Text, StringVar
from src.utils.graphical_utils import LabelEntryPair, Serials, IntVar, Checkbutton
from src.utils.graphical_utils import Combobox
from src.interface.widgets.schedule_picker import SchedulePicker
from src.interface.widgets.right_click import RCMSerial, RCMStudy
from src.interface.widgets.agenda_canvas import WorkingFrame
from src.interface.widgets.footer_grad import FooterFrame

# -------------------------------------------------------------------#


class StudiesTemplate(Frame):
    """
    Contains the Frame in which will be displayed every
    templates related to the studies.
    """

    def __init__(self, body=None):
        super().__init__(body, bg="#5b557f")
        self.manager = body
        self.db_manager = body.manager.manager.gui.app.db_cursor
        self.pack(fill='both', expand=True, side='top')
        self.update_idletasks()

        self.time_interval = 50  # 24 hours
        self.starting_time = 0

        self.days_off_frame = None
        self.study_frame = None
        self.add_study = None
        self.add_days_off = None

        self.setup_timelines()

        self.compact_btn = ButtonApp(self, text="Compacter",
                                     command=self.compact_navbar, custom_theme="Green")
        self.compact_btn.grid(row=0, column=0, sticky='nsew')

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=12)
        self.rowconfigure(2, weight=12)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)

    def setup_timelines(self, day_of_week=None) -> None:
        """
        Setup the timelines.
        """
        self.days_off_frame = self.setup_off_days_frame()
        self.study_frame = self.setup_studies_frame()
        self.footer_frame = FooterFrame(self, self.study_frame,
                                        self.days_off_frame, day_of_week)
        self.footer_frame.canvas.configure(
            scrollregion=self.footer_frame.canvas.bbox('all'))

    def update_timelines(self, _start_date: int, time_interval: int, _day_of_week: str) -> None:
        """
        Updates the graduation of the timelines.
        """
        self.time_interval = time_interval

        self.days_off_frame.destroy()
        self.study_frame.destroy()
        self.footer_frame.destroy()

        self.setup_timelines(_day_of_week)

    def compact_navbar(self) -> None:
        """
        Compacts the navbar to the left of the screen.
        """
        self.days_off_frame.grid_forget()
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=12)
        self.rowconfigure(3, weight=1)
        self.compact_btn.config(text="Etendre", command=self.expand_navbar)

    def expand_navbar(self) -> None:
        """
        Expands the navbar to the left of the screen.
        """
        self.compact_btn.config(text="Compacter", command=self.compact_navbar)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=12)
        self.rowconfigure(2, weight=12)
        self.rowconfigure(3, weight=1)
        self.days_off_frame.grid(row=1, column=0, sticky='nsew', pady=(0, 10))

    def setup_off_days_frame(self) -> None:
        """
        Setup the template of days off.
        """
        return DaysOffTimelineTemplate(self, row=1)

    def setup_studies_frame(self) -> None:
        """
        Setup the template of studies.
        """
        return StudyTimelineTemplate(self, row=2)

    def from_addstudy_to_studies_frame(self) -> None:
        """
        Back to the studies frame.
        """
        self.manager.manager.header.reset_modifications()
        self.add_study.pack_forget()
        self.add_study = None
        self.manager.manager.footer.show_filters()
        self.study_frame.grid(row=2, column=0, sticky='nsew', pady=(0, 10))
        self.days_off_frame.grid(row=1, column=0, sticky='nsew', pady=(0, 10))
        self.compact_btn.grid(row=0, column=0, sticky='nsew')
        self.footer_frame.grid(row=3, column=0, sticky='nsew')

    def from_adddaysoff_to_studies_frame(self) -> None:
        """
        Back to the studies frame.
        """
        self.manager.manager.header.reset_modifications()
        self.add_days_off.pack_forget()
        self.add_days_off = None
        self.manager.manager.footer.show_filters()
        self.study_frame.grid(row=2, column=0, sticky='nsew', pady=(0, 10))
        self.days_off_frame.grid(row=1, column=0, sticky='nsew', pady=(0, 10))
        self.compact_btn.grid(row=0, column=0, sticky='nsew')
        self.footer_frame.grid(row=3, column=0, sticky='nsew')

    def setup_add_study(self) -> None:
        """
        Setup the template of adding a study.
        """
        if self.add_study is not None:
            return
        self.manager.manager.footer.hide_filters()
        self.study_frame.grid_forget()
        self.days_off_frame.grid_forget()
        self.footer_frame.grid_forget()
        self.compact_btn.grid_forget()
        self.add_study = AddStudyTemplate(self)
        self.add_study.pack(fill='both', expand=True,
                            side='top', padx=10, pady=10)

    def setup_add_days_off(self) -> None:
        """
        Setup the template of adding days off.
        """
        if self.add_days_off is not None:
            return
        self.manager.manager.footer.hide_filters()
        self.study_frame.grid_forget()
        self.days_off_frame.grid_forget()
        self.footer_frame.grid_forget()
        self.compact_btn.grid_forget()
        self.add_days_off = AddDaysOffTemplate(self)
        self.add_days_off.pack(fill='both', expand=True,
                               side='top', padx=10, pady=10)

# -------------------------------------------------------------------#


class DaysOffTimelineTemplate(WorkingFrame):
    """
    Contains the timeline of the days off.
    """

    def __init__(self, body, row):
        super().__init__(body, row=row)
        self.manager = body
        self.update_idletasks()
        self.right_click_menu_study = RCMStudy(self)
        self.bind("<Button-3>", self.right_click_menu_study.show)


# -------------------------------------------------------------------#

class StudyTimelineTemplate(WorkingFrame):
    """
    Contains the timeline of the days off.
    """

    def __init__(self, body, row):
        super().__init__(body, row=row)
        self.manager = body
        self.update_idletasks()
        self.right_click_menu_study = RCMStudy(self)
        self.right_click_menu_serial = RCMSerial(self)
        
        for study in self.retrieve_studies():
            study_frame = self.add_study(study["name"], study["archived"],
                                         study["client_name"], study["number"],
                                         study["animal_type_id"], study["description"])
            # for serial in self.manager.db_manager.get_serials(study["id"]):
            #     serial_frame = self.add_serial(study_frame, serial["name"])
            #     for task in self.manager.db_manager.get_tasks(serial["id"]):
            #         self.add_task(serial_frame, task["name"], task["start_date"], task["end_date"])
        
        # self.manager.db_manager.insert_study("STUDY TEST", 0, "CLIENT TEST", 1, 69, "Lorem ipsum")
        # self.add_study("STUDY TEST", 0, "CLIENT TEST", 1, 69, "Lorem ipsum")
        # serial_frame = self.add_serial(study_frame, "SERIAL TEST")
        # self.manager.db_manager.insert_task(1, 1, 1, 1, 1, 1, datetime(2023, 7, 16, 10, 0), datetime(2023, 7, 16, 18, 0),
        #                                     "Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
        # self.add_task(serial_frame, "TASK TEST", datetime(2023, 7, 16, 10, 0), datetime(2023, 7, 16, 18, 0))
        
    def retrieve_studies(self) -> list:
        """
        Retrieves the studies from the database.
        """
        return self.manager.db_manager.get_studies()

# -------------------------------------------------------------------#


class AddStudyTemplate(Frame):
    """
    Templates displayed when the user wants to add a study.
    """

    def __init__(self, study_template) -> None:
        super().__init__(study_template)
        self.manager = study_template
        self.db_cursor_manager = study_template.manager.manager.manager.gui.app.db_cursor
        self.configure(bg="#FFFFFF")

        self.study_name = LabelEntryPair(self, "Study name")
        self.study_name.pack(fill='both', side='top', padx=10)
        
        self.client_name = LabelEntryPair(self, "Client name")
        self.client_name.pack(fill='both', side='top', padx=10)
        
        self.number = LabelEntryPair(self, "Number") 
        self.number.pack(fill='both', side='top', padx=10)
        
        
        options = [animal_type["name"] for
                   animal_type in self.db_cursor_manager.get_animal_types()]
        self.animal_type = StringVar()
        Combobox(self, textvariable=self.animal_type, values=options,
                               state="readonly", width=30).pack()
        self.animal_type.set(options[0])

        self.checkbox_var = IntVar()
        self.checkbox = Checkbutton(self, text="Archived", bg="#FFFFFF", activebackground="#FFFFFF",
                                    variable=self.checkbox_var, command=None)
        self.checkbox.pack(side='top', padx=10, pady=10, anchor="w")

        # Description of the study
        Label(self, text="Description", bg="#FFFFFF").pack(
            fill='both', side='top', padx=10)
        self.description = Text(self)
        self.description.pack(fill='both', side='top', padx=10)

        # Serials of the study
        self.serials = Serials(self)
        self.serials.pack(fill='both', side='top', padx=10, pady=10)

        # Bottom widget
        self.bottom_frame = Frame(self, bg="white")
        self.bottom_frame.pack(fill='both', side='bottom', padx=10, pady=10)
        self.confirm_btn = ButtonApp(self.bottom_frame, text="Confirm",
                                     command=lambda: self.confirm(
                                        self.study_name.entry.get(), self.client_name.entry.get(),
                                        self.number.entry.get(), self.animal_type.get(),
                                        self.checkbox_var.get(),
                                        self.description.get("1.0", "end-1c")
                                  ))
        self.back_btn = ButtonApp(self.bottom_frame, text="Back",
                                  command=self.manager.from_addstudy_to_studies_frame)
        self.confirm_btn.pack(fill='both', expand=True,
                              side='left', padx=10, pady=10)
        self.back_btn.pack(fill='both', expand=True,
                           side='left', padx=10, pady=10)

    def confirm(self, study_name: str, client_name: str, number: int,
                animal_type: str, archived: bool, description: str) -> None:
        """
        Confirms the creation of the study.
        """
        self.db_cursor_manager.insert_study(study_name, client_name, 
            number, animal_type, archived, description)
        self.manager.from_addstudy_to_studies_frame()
        self.master.update_timelines(self.master.starting_time, self.master.time_interval, None)
        
# -------------------------------------------------------------------#


class AddDaysOffTemplate(Frame):
    """
    Templates displayed when the user wants to add a study.
    """
    parameters = ["Title", "Operator", "Color"]

    def __init__(self, study_template) -> None:
        super().__init__(study_template)
        self.manager = study_template
        self.configure(bg="#FFFFFF")

        self.daysoff_title = LabelEntryPair(self, "Title")
        self.daysoff_title.pack(fill='both', side='top', padx=10)
        self.daysoff_operator = LabelEntryPair(self, "Operator")
        self.daysoff_operator.pack(fill='both', side='top', padx=10)

        ButtonApp(self, text="COLOR",
                  command=self.choose_color).pack(side="top")

        self.checkbox_var = IntVar()
        self.checkbox = Checkbutton(self, text="Force", bg="#FFFFFF", activebackground="#FFFFFF",
                                    variable=self.checkbox_var, command=None)
        self.checkbox.pack(side='top', padx=10, pady=10, anchor="w")

        # agenda of the study
        self.agenda_canvas = Canvas(self, bg="gold")
        self.agenda_canvas.pack(fill='both', side='top', padx=10, pady=10)

        # Schedule picker
        self.schedule_selector = SchedulePicker(self)
        self.schedule_selector.pack(side="left")

        # Bottom widget
        self.bottom_frame = Frame(self, bg="white")
        self.bottom_frame.pack(fill='both', side='bottom', padx=10, pady=10)
        self.confirm_btn = ButtonApp(self.bottom_frame, text="Confirm",
                                     command=self.manager.from_adddaysoff_to_studies_frame)
        self.back_btn = ButtonApp(self.bottom_frame, text="Back",
                                  command=self.manager.from_adddaysoff_to_studies_frame)
        self.confirm_btn.pack(fill='both', expand=True,
                              side='left', padx=10, pady=10)
        self.back_btn.pack(fill='both', expand=True,
                           side='left', padx=10, pady=10)

    def choose_color(self) -> None:
        """
        Opens a color picker.
        returns the color chosen.
        """
        color = askcolor()
        if color:
            self.config(bg=color[1])

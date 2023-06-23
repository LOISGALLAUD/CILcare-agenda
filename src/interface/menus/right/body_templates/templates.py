"""
template.py

This file contains the template template.
"""

#------------------------------------------------------------------------------#

from tkcolorpicker import askcolor
from src.utils.graphical_utils import Frame, Label, Canvas, Combobox, Text, StringVar, Scrollbar
from src.utils.graphical_utils import LabelEntryPair, IntVar, Checkbutton, ButtonApp
from src.interface.widgets.right_click import RCMTemplates
from src.interface.widgets.schedule_picker import SchedulePicker

#------------------------------------------------------------------------------#

class TemplatesTemplate(Frame):
    """
    Template page of the agenda.
    """
    def __init__(self, body:Frame) -> None:
        super().__init__(body)
        self.configure(bg='red')
        self.manager = body
        self.db_cursor_manager = self.manager.manager.manager.gui.app.db_cursor
        self.template_examples = self.db_cursor_manager.get_templates()
        self.configure(bg="white")
        self.propagate(False)

        self.templates_timeline = TemplateTimeline(self)
        self.add_task_template = TaskTemplate(self)
        self.templates_timeline.pack(fill="both", expand=True, side="top")
        self.add_templates_template = None

    def from_timeline_to_add_templates(self):
        """
        Switches from the timeline to the add templates template.
        """
        if self.add_templates_template:
            self.add_templates_template.destroy()
        self.templates_timeline.pack_forget()
        self.setup_add_template()

    def from_add_templates_to_timeline(self):
        """
        Switches from the add templates template to the timeline.
        """
        self.add_templates_template.destroy()
        self.templates_timeline.pack(fill="both", expand=True, side="top")

    def setup_add_template(self):
        """
        Adds an template to the templates page.
        """
        self.add_templates_template = AddTemplateTemplate(self)
        self.add_templates_template.pack(fill='both', expand=True, side='top')

    def clear_timeline(self):
        """
        Clears the timeline.
        """
        for child in self.templates_timeline.winfo_children():
            child.destroy()

    def from_timeline_to_add_tasks(self):
        """
        Switch from timeline to add tasks.
        """
        self.templates_timeline.destroy()
        self.add_task_template.pack(fill="both", expand=True, side="top")

    def from_add_task_to_timeline(self):
        """
        Switches from the add tasks template to the timeline.
        """
        self.add_task_template.destroy()
        self.templates_timeline.pack(fill="both", expand=True, side="top")

class TemplateTimeline(Frame):
    """
    Contains templates names and their disponibilities
    in a timeline.
    """
    def __init__(self, manager=None) -> None:
        """
        Setup the lines of the templates page.
        Contains templates names on the left
        and their disponibilities on the right.
        """
        super().__init__(manager)
        self.manager = manager
        self.right_click_menu = RCMTemplates(self)
        self.setup_timeline()

    def setup_timeline(self) -> None:
        """
        Setup the timeline of the templates page.
        """
        for template in self.manager.template_examples:
            line_frame = Frame(self)
            line_frame.propagate(False)
            line_frame.rowconfigure(0, weight=1)
            line_frame.columnconfigure(0, weight=1)
            line_frame.columnconfigure(1, weight=4)
            line_frame.pack(fill="both", expand=True, side="top")
            Label(line_frame, text=template["study_name"]).pack(side="left", fill="both")
            canvas = Canvas(line_frame, width=100,  height=100, bg="red")
            canvas.pack(side="right", fill="both", expand=True)
            canvas.bind("<Button-3>", self.right_click_menu.show)

class TaskTemplate(Frame):
    """
    Task frame displayed when right clicked.
    """
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager
        self.config(bg="white")
        self.task_name = None
        self.checkboxes = None
        self.setup_widgets()

    def setup_widgets(self):
        """
        Setup the widgets of the task template.
        """
        self.task_name = LabelEntryPair(self, "Task name")
        self.task_name.pack(fill="both", side="top")
        Label(self, text="Template name (where is clicked)", bg="#FFFFFF").pack(side='top', padx=10)
        ButtonApp(self, text="COLOR",
                  command=self.choose_color).pack(side="top")

        # Qualifications allowed
        frame = Frame(self, bg="white")
        frame.pack(side='top')
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        canvas = Canvas(frame, yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both")
        scrollbar.config(command=canvas.yview)
        inner_frame = Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor='nw')

        # Adding the checkboxes
        self.checkboxes = []
        for qual in self.manager.db_cursor_manager.get_qualifications():
            var = IntVar()
            checkbutton = Checkbutton(inner_frame, text=qual["name"],
                                      variable=var)
            self.checkboxes.append((qual["id"], var))
            checkbutton.pack(anchor='w')
        inner_frame.bind('<Configure>',
                         lambda event: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>',
                    lambda event: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind_all("<MouseWheel>",
                        lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        agenda_canvas = Canvas(self, width=100, height=100, bg="gold")
        agenda_canvas.pack(side="top")

        # Schedule picker
        self.schedule_selector = SchedulePicker(self)
        self.schedule_selector.pack(side="left")

        # Force checkbox
        self.checkbox_var = IntVar()
        self.checkbox_force = Checkbutton(self, text="Force",
                                          bg="#FFFFFF", activebackground="#FFFFFF",
                                          variable=self.checkbox_var, command=None)
        self.checkbox_force.pack(side='left', padx=10, pady=10, anchor="w")

        # Bottom widget
        self.bottom_frame = Frame(self, bg="white")
        self.bottom_frame.pack(fill='both', side='bottom', padx=10, pady=10)
        self.confirm_btn = ButtonApp(self.bottom_frame, text="Confirm",
                                     command=None)
        self.back_btn = ButtonApp(self.bottom_frame, text="Back",
                                  command=self.manager.from_add_task_to_timeline)
        self.confirm_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)
        self.back_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)

    def get_checked_vars(self) -> list:
        """
        Returns the checked vars of the checkboxes.
        """
        checked_vars = []
        for qual_id, var in self.checkboxes:
            if var.get():
                checked_vars.append(qual_id)
        return checked_vars

    def choose_color(self):
        """
        Opens a color picker.
        returns the color chosen.
        """
        color = askcolor()
        if color:
            self.config(bg=color[1])

#-------------------------------------------------------------------#

class AddTemplateTemplate(Frame):
    """
    Add templates template.
    """
    def __init__(self, body=None):
        super().__init__(body)
        self.manager = body
        self.configure(bg="pink")
        self.propagate(False)

        self.setup_widgets()

    def setup_widgets(self) -> None:
        """
        Setup the widgets of the add templates template.
        """
        self.template_name = LabelEntryPair(self, "Template name")
        self.template_name.pack(fill="both", side="top")

        # animal_type widget
        options = [animal_type["name"] for
                   animal_type in self.manager.db_cursor_manager.get_animal_types()]
        self.animal_type = StringVar()
        Combobox(self, textvariable=self.animal_type, values=options,
                               state="readonly", width=30).pack()
        self.animal_type.set(options[0])

        Label(self, text="Description", bg="#FFFFFF").pack(side='top', padx=10)
        self.description = Text(self)
        self.description.pack(fill='both', side='top', padx=10)

        self.checkbox_var = IntVar()
        self.checkbox = Checkbutton(self, text="Archived", bg="#FFFFFF", activebackground="#FFFFFF",
                               variable=self.checkbox_var, command=None)
        self.checkbox.pack(side='top', padx=10, pady=10, anchor="w")

        # Bottom widget
        self.bottom_frame = Frame(self, bg="white")
        self.bottom_frame.pack(fill='both', side='bottom', padx=10, pady=10)
        self.confirm_btn = ButtonApp(self.bottom_frame, text="Confirm",
                                     command=self.confirm)
        self.back_btn = ButtonApp(self.bottom_frame, text="Back",
                                  command=self.manager.from_add_templates_to_timeline)
        self.confirm_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)
        self.back_btn.pack(fill='both', expand=True, side='left', padx=10, pady=10)

    def confirm(self):
        """
        Inserts a room in the database.
        """
        study_name = self.template_name.entry.get()
        archived = self.checkbox_var.get()
        animal_type_id = self.manager.db_cursor_manager.get_animal_types(
            self.animal_type.get())[0]["id"]
        description = self.description.get("1.0", "end-1c")

        self.manager.db_cursor_manager.insert_template(study_name, archived,
                                                       animal_type_id, description)

        self.manager.template_examples = self.manager.db_cursor_manager.get_templates()
        self.manager.clear_timeline()
        self.manager.templates_timeline.setup_timeline()
        self.manager.from_add_templates_to_timeline()

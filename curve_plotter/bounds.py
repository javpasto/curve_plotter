import utility
import wx
import user_interface

class Bounds():
    #Ui text edit functions
    x_lower_bound_ui_edit = user_interface.MyTextCtrl()
    y_lower_bound_ui_edit = user_interface.MyTextCtrl()
    z_lower_bound_ui_edit = user_interface.MyTextCtrl()
    x_upper_bound_ui_edit = user_interface.MyTextCtrl()
    y_upper_bound_ui_edit = user_interface.MyTextCtrl()
    z_upper_bound_ui_edit = user_interface.MyTextCtrl()

    #Text from ui edits
    x_lower_bound_text = None
    y_lower_bound_text = None
    z_lower_bound_text = None
    x_upper_bound_text = None
    y_upper_bound_text = None
    z_upper_bound_text = None

    x_lower_bound_value = utility.DEFAULT_LOWER_AXIS_BOUND
    y_lower_bound_value = utility.DEFAULT_LOWER_AXIS_BOUND
    z_lower_bound_value = utility.DEFAULT_LOWER_AXIS_BOUND
    x_upper_bound_value = utility.DEFAULT_UPPER_AXIS_BOUND
    y_upper_bound_value = utility.DEFAULT_UPPER_AXIS_BOUND
    z_upper_bound_value = utility.DEFAULT_UPPER_AXIS_BOUND

    x_bounds = None
    y_bounds = None
    z_bounds = None

    plot_2d = None

    def initialize(self, plot_2d):
        if (self.x_lower_bound_ui_edit.GetValue() != ''):
            self.x_lower_bound_text = self.x_lower_bound_ui_edit.GetValue()
            self.x_lower_bound_value = float(self.x_lower_bound_text)
        if (self.y_lower_bound_ui_edit.GetValue() != ''):
            self.y_lower_bound_text = self.y_lower_bound_ui_edit.GetValue()
            self.y_lower_bound_value = float(self.y_lower_bound_text)
        if (self.z_lower_bound_ui_edit.GetValue() != ''):
            self.z_lower_bound_text = self.z_lower_bound_ui_edit.GetValue()
            self.z_lower_bound_value = float(self.z_lower_bound_text)
        if (self.x_upper_bound_ui_edit.GetValue() != ''):
            self.x_upper_bound_text = self.x_upper_bound_ui_edit.GetValue()
            self.x_upper_bound_value = float(self.x_upper_bound_text)
        if (self.y_upper_bound_ui_edit.GetValue() != ''):
            self.y_upper_bound_text = self.y_upper_bound_ui_edit.GetValue()
            self.y_upper_bound_value = float(self.y_upper_bound_text)
        if (self.z_upper_bound_ui_edit.GetValue() != ''):
            self.z_upper_bound_text = self.z_upper_bound_ui_edit.GetValue()
            self.z_upper_bound_value = float(self.z_upper_bound_text)

        self.plot_2d = False
        if plot_2d:
            self.plot_2d = True

    def translate(self):
        self.x_lower_bound_text = utility.replace_letters(self.x_lower_bound_text)
        self.y_lower_bound_text = utility.replace_letters(self.y_lower_bound_text)
        self.z_lower_bound_text = utility.replace_letters(self.z_lower_bound_text)
        self.x_upper_bound_text = utility.replace_letters(self.x_upper_bound_text)
        self.y_upper_bound_text = utility.replace_letters(self.y_upper_bound_text)
        self.z_upper_bound_text = utility.replace_letters(self.z_upper_bound_text)

    def create_bounds(self):
        self.x_bounds = [float(self.x_lower_bound_value), float(self.x_upper_bound_value)]
        self.y_bounds = [float(self.y_lower_bound_value), float(self.y_upper_bound_value)]

        if (self.plot_2d != True):
            self.z_bounds = [float(self.z_lower_bound_value), float(self.z_upper_bound_value)]

    def clean(self):
        self.x_lower_bound_text = None
        self.y_lower_bound_text = None
        self.z_lower_bound_text = None
        self.x_upper_bound_text = None
        self.y_upper_bound_text = None
        self.z_upper_bound_text = None

        self.x_lower_bound_value = utility.DEFAULT_LOWER_AXIS_BOUND
        self.y_lower_bound_value = utility.DEFAULT_LOWER_AXIS_BOUND
        self.z_lower_bound_value = utility.DEFAULT_LOWER_AXIS_BOUND
        self.x_upper_bound_value = utility.DEFAULT_UPPER_AXIS_BOUND
        self.y_upper_bound_value = utility.DEFAULT_UPPER_AXIS_BOUND
        self.z_upper_bound_value = utility.DEFAULT_UPPER_AXIS_BOUND

        self.x_bounds = None
        self.y_bounds = None
        self.z_bounds = None

        self.plot_2d = None
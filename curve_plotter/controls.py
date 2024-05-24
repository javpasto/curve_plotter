import utility
import wx
import user_interface


class Controls(wx.App):
    
    steps_ui_edit = user_interface.MyTextCtrl()
    steps_value = utility.DEFAULT_STEPS

    plot_2d_ui_checkbox = user_interface.MyCheckBox()
    plot_2d_checked = None

    plot_ui_button = user_interface.MyButton()

    def initialize(self):
        if (self.steps_ui_edit.GetValue() != ''):
            self.steps_value = float(self.steps_ui_edit.GetValue())
        
        self.plot_2d_checked = self.plot_2d_ui_checkbox.IsChecked()

    def clean(self):
        self.steps_value = utility.DEFAULT_STEPS

        self.plot_2d_checked = None
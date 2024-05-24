import utility
import wx
import user_interface

class Vector():
    #Ui curve name
    vector_name_ui_edit = user_interface.MyTextCtrl()

    #Text form ui edits
    vector_name = None

    #Ui text edit functions
    ini_point_ui_edit = user_interface.MyTextCtrl()
    value_ui_edit = user_interface.MyTextCtrl()

    #Text from ui edits
    ini_point_text = None
    value_text = None

    #Real Values
    ini_point_value = None
    value_value = None

    #Color cmb
    vector_color_ui_combo = user_interface.MyComboBox()

    vector_color_text = None

    def initialize(self):
        if self.vector_name_ui_edit.GetValue() == '':
            return False
        
        self.vector_name = self.vector_name_ui_edit.GetValue()

        if (self.ini_point_ui_edit.GetValue() != ''):
            self.ini_point_text = self.ini_point_ui_edit.GetValue()
            string = self.ini_point_ui_edit.GetValue().replace('(', '').replace(')', '').split(',')
            self.ini_point_value = []

            for i in range(0, len(string)):
                self.ini_point_value.append(float(string[i]))
        else:
            raise utility.ControlException('Init point needs a value for vector ' + self.vector_name + '.')

        if (self.value_ui_edit.GetValue() != ''):
            self.value_text = self.value_ui_edit.GetValue()
            string = self.value_ui_edit.GetValue().replace('(', '').replace(')', '').split(',')
            self.value_value = []

            for i in range(0, len(string)):
                self.value_value.append(float(string[i]))
        else:
            raise utility.ControlException('Value needs a value for vector ' + self.vector_name + '.')
        
        if self.vector_color_ui_combo.GetValue() == '':
            self.vector_color_text = utility.DEFAULT_VECTOR_COLOR
        else:
            self.vector_color_text = utility.COLORS_GRAPH[utility.COLORS_USER_INTERFACE.index(self.vector_color_ui_combo.GetValue())]


    def translate(self):
        self.vector_name = utility.replace_letters(self.vector_name)
        self.ini_point_text = utility.replace_letters(self.ini_point_text)
        self.value_text = utility.replace_letters(self.value_text)

    def clean(self):
        self.vector_name = None

        self.ini_point_text = None
        self.value_text = None

        self.ini_point_value = None
        self.value_value = None

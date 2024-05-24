import utility
import wx
import user_interface
import tree

class Curve():
    #Ui curve name
    curve_name_ui_edit = user_interface.MyTextCtrl()

    #Text form ui edits
    curve_name = None

    #Ui text edit functions
    x_function_ui_edit = user_interface.MyTextCtrl()
    y_function_ui_edit = user_interface.MyTextCtrl()
    z_function_ui_edit = user_interface.MyTextCtrl()

    #Text from ui edits
    x_function_text = None
    y_function_text = None
    z_function_text = None

    #Generated trees from ui functions
    x_tree = tree.Tree()
    y_tree = tree.Tree()
    z_tree = tree.Tree()

    #Np arrays with values
    x = None
    y = None
    z = None

    #Color cmb
    curve_color_ui_combo = user_interface.MyComboBox()

    curve_color_text = None

    #Number of dimensions
    dimensions = None

    def initialize(self):
        if (self.curve_name_ui_edit.GetValue() == ''):
            return False
        
        self.curve_name = self.curve_name_ui_edit.GetValue()

        if (self.x_function_ui_edit.GetValue() != ''):
            self.x_function_text = self.x_function_ui_edit.GetValue()
        
        if (self.y_function_ui_edit.GetValue() != ''):
            self.y_function_text = self.y_function_ui_edit.GetValue()

        if (self.z_function_ui_edit.GetValue() != ''):
            self.z_function_text = self.z_function_ui_edit.GetValue()

        if self.curve_color_ui_combo.GetValue() == '':
            self.curve_color_text = utility.DEFAULT_CURVE_COLOR
        else:
            self.curve_color_text = utility.COLORS_GRAPH[utility.COLORS_USER_INTERFACE.index(self.curve_color_ui_combo.GetValue())]

    def translate(self):
        self.curve_name = utility.replace_letters(self.curve_name)
        self.x_function_text = utility.replace_letters(self.x_function_text)
        self.y_function_text = utility.replace_letters(self.y_function_text)
        self.z_function_text = utility.replace_letters(self.z_function_text)

    def create_trees(self, parameter_names):
        if self.curve_name is not None:
            self.x_tree = tree.tree_generator(self.x_function_text, parameter_names)
            self.y_tree = tree.tree_generator(self.y_function_text, parameter_names)
            self.z_tree = tree.tree_generator(self.z_function_text, parameter_names)

    def solve_trees(self, steps, parameters, parameter_names):
        if self.curve_name is None:
            return
        
        if self.x_tree is not None:
            self.x_tree.initialize_tree(steps=steps, parameters=parameters, parameter_names=parameter_names)
            self.x = self.x_tree.resolve_tree()
        if self.y_tree is not None:
            self.y_tree.initialize_tree(steps=steps, parameters=parameters, parameter_names=parameter_names)
            self.y = self.y_tree.resolve_tree()
        if self.z_tree is not None:
            self.z_tree.initialize_tree(steps=steps, parameters=parameters, parameter_names=parameter_names)
            self.z = self.z_tree.resolve_tree()

    def clean(self):

        self.curve_name = None

        self.x_function_text = None
        self.y_function_text = None
        self.z_function_text = None

        self.x_tree = None
        self.y_tree = None
        self.z_tree = None

        self.x = None
        self.y = None
        self.z = None

        self.dimensions = None
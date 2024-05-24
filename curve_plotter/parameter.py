import utility
import wx
import user_interface
import numpy as np
import tree

class Parameter():

    #Ui curve name
    parameter_name_ui_edit = user_interface.MyTextCtrl()

    #Text form ui edits
    parameter_name = None

    #Ui text edit functions
    lower_bound_ui_edit = user_interface.MyTextCtrl()
    upper_bound_ui_edit = user_interface.MyTextCtrl()

    #Text from ui edits
    lower_bound_text = None
    upper_bound_text = None

    value_array = None

    def initialize(self, steps):
        
        if (self.parameter_name_ui_edit.GetValue() == ''):
            return False
        
        self.parameter_name = self.parameter_name_ui_edit.GetValue()

        if (self.upper_bound_ui_edit.GetValue() == ''):
            #A single value parameter
            if (self.lower_bound_ui_edit.GetValue() == ''):
                #Expected at least a value!
                raise utility.ControlException('Expected at least one value (lower) for ' + self.parameter_name + '.')
                return False
            
            self.lower_bound_text = self.lower_bound_ui_edit.GetValue()

            aux_tree = tree.Tree()
            aux_tree = tree.tree_generator(self.lower_bound_text, self.parameter_name)
            aux_tree.initialize_tree(steps=1, parameter_names=[self.parameter_name])
            value_tree = aux_tree.resolve_tree()[0]
            self.value_array = np.linspace(value_tree, value_tree, steps)

        else:
            self.lower_bound_text = self.lower_bound_ui_edit.GetValue()
            self.upper_bound_text = self.upper_bound_ui_edit.GetValue()

            aux_tree = tree.Tree()
            aux_tree = tree.tree_generator(self.lower_bound_text, self.parameter_name)
            aux_tree.initialize_tree(steps=1, parameter_names=[self.parameter_name])
            value_tree = aux_tree.resolve_tree()[0]

            aux_tree = tree.tree_generator(self.upper_bound_text, self.parameter_name)
            aux_tree.initialize_tree(steps=1, parameter_names=[self.parameter_name])
            value_tree_2 = aux_tree.resolve_tree()[0]

            self.value_array = np.linspace(value_tree, value_tree_2, steps)

        return True

    def translate(self):
        self.parameter_name = utility.replace_letters(self.parameter_name)
        self.lower_bound_text = utility.replace_letters(self.lower_bound_text)
        self.upper_bound_text = utility.replace_letters(self.upper_bound_text)

    def clean(self):
        self.parameter_name = None

        self.lower_bound_text = None
        self.upper_bound_text = None

        self.value_array = None

'''
author: Javier Pastor Ramirez
'''

from mpl_toolkits import mplot3d
#%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import math
import wx
import ast
from sympy import symbols, cos, dotprint
from graphviz import Source
from matplotlib import colors
import matplotlib.patches as mpatches

import utility
import vector
import controls
import bounds
import parameter
import curve
import user_interface

class MyFrame(wx.Frame):

    #Curves
    curves = [curve.Curve(), curve.Curve()]

    #Parameters
    parameters = [parameter.Parameter(), parameter.Parameter(), parameter.Parameter()]

    #Vectors
    vectors = [vector.Vector(), vector.Vector(), vector.Vector()]

    #Graph bounds
    bounds = bounds.Bounds()

    #Controls
    controls = controls.Controls()

    #Plotter for Graph
    plotter = plt

    #Sets up the user interface
    def __init__(self):
        super().__init__(parent=None, title='Curve Plotter')

        #For the row heights
        counter = 0

        #Curves
        for i in range(0, len(self.curves)):
            self.curves[i].curve_name_ui_edit = user_interface.MyTextCtrl(self, 'curve name', (utility.FIRST_COLUMN, utility.USER_INTERFACE_MARGINS + utility.SPACING_ROWS*counter)) 
            self.curves[i].x_function_ui_edit = user_interface.MyTextCtrl(self, 'x function', (utility.SECOND_COLUMN, utility.USER_INTERFACE_MARGINS + utility.SPACING_ROWS*counter))
            self.curves[i].y_function_ui_edit = user_interface.MyTextCtrl(self, 'y function', (utility.THIRD_COLUMN, utility.USER_INTERFACE_MARGINS + utility.SPACING_ROWS*counter))
            self.curves[i].z_function_ui_edit = user_interface.MyTextCtrl(self, 'z function', (utility.FOURTH_COLUMN, utility.USER_INTERFACE_MARGINS + utility.SPACING_ROWS*counter))
            self.curves[i].curve_color_ui_combo = user_interface.MyComboBox(self, pos=(utility.FIFTH_COLUMN, utility.USER_INTERFACE_MARGINS + utility.SPACING_ROWS*counter))
            counter += 1

        #Parameters
        for i in range(0, len(self.parameters)):
            self.parameters[i].parameter_name_ui_edit =  user_interface.MyTextCtrl(self, 'parameter name', (utility.FIRST_COLUMN, utility.USER_INTERFACE_MARGINS + utility.SPACING_ROWS*counter)) 
            self.parameters[i].lower_bound_ui_edit = user_interface.MyTextCtrl(self, 'lower bound', (utility.SECOND_COLUMN, utility.USER_INTERFACE_MARGINS + utility.SPACING_ROWS*counter))
            self.parameters[i].upper_bound_ui_edit = user_interface.MyTextCtrl(self, 'upper bound', (utility.THIRD_COLUMN, utility.USER_INTERFACE_MARGINS + utility.SPACING_ROWS*counter))
            counter += 1

        #Vectors
        for i in range(0, len(self.vectors)):
            self.vectors[i].vector_name_ui_edit =  user_interface.MyTextCtrl(self, 'vector name', (utility.FIRST_COLUMN, utility.USER_INTERFACE_MARGINS + utility.SPACING_ROWS*counter)) 
            self.vectors[i].ini_point_ui_edit = user_interface.MyTextCtrl(self, 'init point', (utility.SECOND_COLUMN, utility.USER_INTERFACE_MARGINS + utility.SPACING_ROWS*counter))
            self.vectors[i].value_ui_edit = user_interface.MyTextCtrl(self, 'value', (utility.THIRD_COLUMN, utility.USER_INTERFACE_MARGINS + utility.SPACING_ROWS*counter))
            self.vectors[i].vector_color_ui_combo = user_interface.MyComboBox(self, pos=(utility.FOURTH_COLUMN, utility.USER_INTERFACE_MARGINS + utility.SPACING_ROWS*counter))
            counter += 1

        #Graph Bounds
        self.bounds.x_lower_bound_ui_edit = user_interface.MyTextCtrl(self, 'x graph lower bound', (utility.FIRST_COLUMN, utility.USER_INTERFACE_MARGINS + utility.SPACING_ROWS*counter))
        self.bounds.y_lower_bound_ui_edit = user_interface.MyTextCtrl(self, 'y graph lower bound', (utility.SECOND_COLUMN, utility.USER_INTERFACE_MARGINS + utility.SPACING_ROWS*counter))
        self.bounds.z_lower_bound_ui_edit = user_interface.MyTextCtrl(self, 'z graph lower bound', (utility.THIRD_COLUMN, utility.USER_INTERFACE_MARGINS + utility.SPACING_ROWS*counter))
        counter += 1

        self.bounds.x_upper_bound_ui_edit = user_interface.MyTextCtrl(self, 'x graph upper bound', (utility.FIRST_COLUMN, utility.USER_INTERFACE_MARGINS + utility.SPACING_ROWS*counter))
        self.bounds.y_upper_bound_ui_edit = user_interface.MyTextCtrl(self, 'y graph upper bound', (utility.SECOND_COLUMN, utility.USER_INTERFACE_MARGINS + utility.SPACING_ROWS*counter))
        self.bounds.z_upper_bound_ui_edit = user_interface.MyTextCtrl(self, 'z graph upper bound', (utility.THIRD_COLUMN, utility.USER_INTERFACE_MARGINS + utility.SPACING_ROWS*counter))
        counter += 1

        #Controls
        self.controls.steps_ui_edit = user_interface.MyTextCtrl(self, 'steps', (utility.FIFTH_COLUMN, utility.USER_INTERFACE_MARGINS + utility.SPACING_ROWS*(counter-3)))
        self.controls.plot_2d_ui_checkbox = wx.CheckBox(self, label='2d plot', pos=(utility.FIFTH_COLUMN + 35, utility.USER_INTERFACE_MARGINS + utility.SPACING_ROWS*(counter-2)))
        self.controls.plot_ui_button = wx.Button(self, label='Plot Curve', pos=(utility.FIFTH_COLUMN + 35, utility.USER_INTERFACE_MARGINS + utility.SPACING_ROWS*(counter-1)))
        counter += 1

        #Bind the function with the ui click
        #Poner el bind en controls!
        self.controls.plot_ui_button.Bind(wx.EVT_BUTTON, self.OnClickButton)

        #Set the window size
        self.Size = (utility.WIDTH, utility.USER_INTERFACE_MARGINS + utility.SPACING_ROWS*(counter))

        self.Show()
    
    #Show a warning message on screen
    def warning_message(self, str):
        msgbox = wx.MessageBox(caption='Warning', message=str, style=0)
        wx.OK
        msgbox.show()

    #True if correctyl initialize, false otherwise
    def initialize(self):

        #Controls
        self.controls.initialize()

        #Bounds
        self.bounds.initialize(self.controls.plot_2d_checked)

        #Parameters
        self.parameter_names = []
        for i in range(0, len(self.parameters)):
            try:
                if self.parameters[i].initialize(self.controls.steps_value):
                    self.parameter_names.append(self.parameters[i].parameter_name)
            except utility.ControlException as err:
                self.warning_message(str(err))
                return False
        
        #Curves
        for i in range(0, len(self.curves)):
            try:
                self.curves[i].initialize()
            except utility.ControlException as err:
                self.warning_message(str(err))
                return False
        
        #Vectors
        for i in range(0, len(self.vectors)):
            try:
                self.vectors[i].initialize()
            except utility.ControlException as err:
                self.warning_message(str(err))
                return False  
            
        #Plotter
        self.plotter = plt

    def translate(self):
        for i in range(0, len(self.curves)):
            self.curves[i].translate()

        for i in range(0, len(self.parameters)):
            self.parameters[i].translate()

        for i in range(0, len(self.parameter_names)):
            self.parameter_names[i] = utility.replace_letters(self.parameter_names[i])
        
        for i in range(0, len(self.vectors)):
            self.vectors[i].translate()

    def create_bounds(self):
        self.bounds.create_bounds()

    def create_trees(self):
        for i in range(0, len(self.curves)):
            self.curves[i].create_trees(self.parameter_names)     

    def build_legend(self):
        self.legend_value = ""
        return
    
        self.legend_value = ALPHA + '('
        self.legend_value += self.parameter_names[0]
        for i in range(1, len(self.parameter_names)):
            self.legend_value += ', ' + self.parameter_names[i]
        self.legend_value += ') = ('

        if (self.x_tree is not None):
            self.legend_value += self.x_tree.to_string()
        
        if (self.y_tree is not None):
            self.legend_value += ', ' + self.y_tree.to_string()
        
        if (self.z_tree is not None):
            self.legend_value += ', ' + self.z_tree.to_string()

        self.legend_value += ')'

        self.legend_value += '\n    | ' + self.parameter_names[0] + ' = (' + self.param_1_legend_bounds[0] + ', ' +  self.param_1_legend_bounds[1] + ')'
        if len(self.parameter_names) > 1:
            self.legend_value += '\n    | ' + self.parameter_names[1] + ' = ' + self.param_2_legend_bounds

    def solve_trees(self):
        parameter_arrays = []
        
        for i in range(0, 3):
            if self.parameters[i] is not None:
                parameter_arrays.append(self.parameters[i].value_array)

        for i in range(0, 2):
            self.curves[i].solve_trees(self.controls.steps_value, parameter_arrays, self.parameter_names)

    def clean_values(self):
        for curve in self.curves:
            curve.clean()
        for parameter in self.parameters:
            parameter.clean()
        for vector in self.vectors:
            vector.clean()
        self.bounds.clean()
        self.controls.clean()

        self.plotter = None

    def plot_vectors(self):
        for i in range(0, len(self.vectors)):
            if self.vectors[i].vector_name is not None:
                label_vect = self.vectors[i].vector_name + ' = ' + self.vectors[i].value_text + ', from ' + self.vectors[i].ini_point_text
                if '(' not in label_vect:
                    label_vect = self.vectors[i].vector_name + ' = (' + self.vectors[i].value_text + '), from (' + self.vectors[i].ini_point_text + ')'
                if self.controls.plot_2d_checked:
                    self.plotter.arrow(x=self.vectors[i].ini_point_value[0], y=self.vectors[i].ini_point_value[1], dx=self.vectors[i].value_value[0], dy=self.vectors[i].value_value[1], color=self.vectors[i].vector_color_text, label=label_vect, head_width=0.2, head_length=0.2)
                else:
                    # Graficar el vector
                    #ax.quiver(0, 0, 0, vector[0], vector[1], vector[2], color='r', label='Vector')
                    self.plotter.quiver(self.vectors[i].ini_point_value[0], self.vectors[i].ini_point_value[1], self.vectors[i].ini_point_value[2], self.vectors[i].value_value[0], self.vectors[i].value_value[1], self.vectors[i].value_value[2], color=self.vectors[i].vector_color_text, label=label_vect)
                    #self.plotter.quiver(self.vectors[i].ini_point_value[0], self.vectors[i].ini_point_value[1], self.vectors[i].ini_point_value[2], (self.vectors[i].value_value[0]+self.vectors[i].ini_point_value[0]), (self.vectors[i].value_value[1]+self.vectors[i].ini_point_value[1]), (self.vectors[i].value_value[2]+self.vectors[i].ini_point_value[2]), color=self.vectors[i].vector_color_text, label=label_vect)
                    #self.plotter.quiver(self.vectors[i].ini_point_value[0], self.vectors[i].ini_point_value[1], self.vectors[i].ini_point_value[2], self.vectors[i].value_value[0], self.vectors[i].value_value[1], self.vectors[i].value_value[2], color=self.vectors[i].vector_color_text, label=label_vect)
    
    def vector_legend(self):
        rtr = ""
        for i in range(0, len(self.vectors)):
            if self.vectors[i].vector_name is not None:
                label_vect = self.vectors[i].vector_name + ' = ' + self.vectors[i].value_text + ', from ' + self.vectors[i].ini_point_text + '\n'
                if '(' not in label_vect:
                    label_vect = self.vectors[i].vector_name + ' = (' + self.vectors[i].value_text + '), from (' + self.vectors[i].ini_point_text + ')\n'
                rtr += label_vect
                
        return rtr


    def plot_curves(self):
        for i in range(0, len(self.curves)):
            if self.curves[i].curve_name is not None:
                if self.controls.plot_2d_checked:
                    label_curv = self.curves[i].curve_name + ' = ($' + self.curves[i].x_function_text + '$, $' + self.curves[i].y_function_text + '$)'
                    self.plotter.plot(self.curves[i].x, self.curves[i].y, color=self.curves[i].curve_color_text, label=label_curv)
                else:
                    label_curv = self.curves[i].curve_name + ' = (' + self.curves[i].x_function_text + ', ' + self.curves[i].y_function_text + ', ' + self.curves[i].z_function_text + ')'
                    self.plotter.plot(self.curves[i].x, self.curves[i].y, self.curves[i].z, color=self.curves[i].curve_color_text, label=label_curv)

    def curve_legend(self):
        rtr = ""
        for i in range(0, len(self.curves)):
            if self.curves[i].curve_name is not None:
                if self.controls.plot_2d_checked:
                    rtr += self.curves[i].curve_name + ' = ($' + self.curves[i].x_function_text + '$, $' + self.curves[i].y_function_text + '$)\n'
                else:
                    rtr = self.curves[i].curve_name + ' = (' + self.curves[i].x_function_text + ', ' + self.curves[i].y_function_text + ', ' + self.curves[i].z_function_text + ')\n'
        return rtr

    def parameter_legend(self):
        rtr = ""

        for parameter in self.parameters:
            if parameter.parameter_name is not None:
                rtr += parameter.parameter_name
                if parameter.upper_bound_text is not None:
                    rtr += ' $\in$ (' + parameter.lower_bound_text + ', ' + parameter.upper_bound_text + ') \n'
                else:
                    rtr += ' = ' + parameter.lower_bound_text + '\n'
        
        return rtr
        dummy_patch = mpatches.Patch(color='none', label='Parameters')
        handles, labels = self.plotter.gca().get_legend_handles_labels()
        handles.append(dummy_patch)
        labels.append(rtr)
        
        self.plotter.legend(handles=handles, labels=labels)

    def plotting_2d(self):
        #Ignore the z axi
        self.plotter = plt
        self.plotter.xlabel('x')
        self.plotter.ylabel('y', rotation=0)
        #self.plotter.plot(self.curves[0].x, self.curves[0].y, color='blue', label=self.legend_value)

        self.plot_curves()

        self.plot_vectors()

        if self.bounds.x_bounds is not None:
            self.plotter.xlim(self.bounds.x_bounds[0], self.bounds.x_bounds[0])
        if self.bounds.y_bounds is not None:
            self.plotter.ylim(self.bounds.y_bounds[0], self.bounds.y_bounds[0])

        #Show parameter legend
        dummy_patch = mpatches.Patch(color='none', label='Parameters')
        handles, labels = self.plotter.gca().get_legend_handles_labels()
        handles.append(dummy_patch)
        labels.append(self.parameter_legend())
        
        self.plotter.legend(handles=handles, labels=labels)

        self.plotter.axis([self.bounds.x_bounds[0], self.bounds.x_bounds[1], self.bounds.y_bounds[0], self.bounds.y_bounds[1]])
        self.plotter.gca().set_aspect('equal', adjustable='box')

        self.plotter.show()

    def plotting(self):

        if self.controls.plot_2d_checked == True:
            self.plotting_2d()
            return
        
        self.plotter = plt.axes(projection='3d')
        self.plotter.set_xlim(self.bounds.x_bounds)
        self.plotter.set_ylim(self.bounds.y_bounds)
        self.plotter.set_zlim(self.bounds.z_bounds)
        
        self.plotter.set_xlabel('x')
        self.plotter.set_ylabel('y')
        self.plotter.set_zlabel('z')

        #Show parameter legend
        dummy_patch = mpatches.Patch(color='none', label='Parameters')
        self.plotter.legend(handles=[dummy_patch], labels=[self.curve_legend() + self.vector_legend() + self.parameter_legend(), 'placeholder_text'])

        self.plot_curves()
        self.plot_vectors()

        #self.plotter.show()
        plt.show()
        #self.plotter.imshow()

    def OnClickButton(self, event):

        #Close the last plot
        self.clean_values()
        plt.close()
        
        #Initialize curves, vectors, parameters, bounds, controls
        self.initialize()

        #Translate special characters
        self.translate()

        #Create bound arrays
        self.create_bounds()

        #Create curve trees
        self.create_trees()

        #Solve curve trees
        self.solve_trees()

        #Plot the results
        self.plotting()

def test():
    # Crear un vector
    # Coordenadas del vector
    X = 2
    Y = 3
    Z = 4
    vector = np.array([X, Y, Z])

    # Crear una figura
    figura = plt.figure()
    ax = figura.add_subplot(111, projection='3d')

    # Graficar el vector
    ax.quiver(0, 0, 0, vector[0], vector[1], vector[2], color='r', label='Vector')

    # Personalizar el gráfico
    ax.set_xlim([0, 5])
    ax.set_ylim([0, 5])
    ax.set_zlim([0, 5])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Representación de un Vector en 3D')
    ax.legend()

    # Mostrar el gráfico
    plt.show()

def Innit():
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()

def quiver_test():

    plotter = plt.axes(projection='3d')
    plotter.set_xlim([-5,5])
    plotter.set_ylim([-5,5])
    plotter.set_zlim([-5,5])
        
    plotter.set_xlabel('x')
    plotter.set_ylabel('y') 
    plotter.set_zlabel('z')

    plotter.quiver(0, 0, 0, 2, 1, 1, color='r', label='quiver_test')
    plt.show()
        

#quiver_test()
Innit()
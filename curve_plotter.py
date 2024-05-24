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

USER_INTERFACE_MARGINS = 10
SPACING_ROWS = 40
FIRST_ROW_HEIGHT = USER_INTERFACE_MARGINS + SPACING_ROWS*0
SECOND_ROW_HEIGHT = USER_INTERFACE_MARGINS + SPACING_ROWS*1
THIRD_ROW_HEIGHT = USER_INTERFACE_MARGINS + SPACING_ROWS*2
FOURTH_ROW_HEIGHT = USER_INTERFACE_MARGINS + SPACING_ROWS*3
FIFTH_ROW_HEIGHT = USER_INTERFACE_MARGINS + SPACING_ROWS*4
SIXTH_ROW_HEIGHT = USER_INTERFACE_MARGINS + SPACING_ROWS*5
SEVENTH_ROW_HEIGHT = USER_INTERFACE_MARGINS + SPACING_ROWS*6
EIGHT_ROW_HEIGHT = USER_INTERFACE_MARGINS + SPACING_ROWS*7
NINTH_ROW_HEIGHT = USER_INTERFACE_MARGINS + SPACING_ROWS*8
TENTH_ROW_HEIGHT = USER_INTERFACE_MARGINS + SPACING_ROWS*9

HEIGHT = 10 + SPACING_ROWS*10

SPACING_COLUMNS = 140
FIRST_COLUMN = 10 + SPACING_COLUMNS*0
SECOND_COLUMN = 10  + SPACING_COLUMNS*1
THIRD_COLUMN = 10 + SPACING_COLUMNS*2
FOURTH_COLUMN = 10 + SPACING_COLUMNS*3
FIFTH_COLUMN = 10 + SPACING_COLUMNS*4

WIDTH = 10 + SPACING_COLUMNS*5

COLORS_GRAPH = ['b', 'c', 'g', 'k', 'm' ,'r' ,'w' ,'y']
COLORS_USER_INTERFACE = ['blue', 'cyan', 'green', 'black', 'magenta', 'red', 'white', 'yellow']
DEFAULT_VECTOR_COLOR = 'r'
DEFAULT_CURVE_COLOR = 'b'

DEFAULT_STEPS = 1000
DEFAULT_LOWER_BOUND = 0
DEFAULT_UPPER_BOUND = 10

DEFAULT_LOWER_AXIS_BOUND = -10
DEFAULT_UPPER_AXIS_BOUND = 10

CONSTANT_PLACEHOLDER = 'CONST'
CONSTANT_VALUE_PLACEHOlDER = 1

ALPHA = '\u03B1'
BETA = '\u03B2'
GAMMA = '\u03B3'
DELTA = '\u03B4	'
RHO = '\u03C1'
PI = '\u03C0'

LETTERS = ['al', 'be', 'ga', 'de', 'ro', 'pi']
LETTERS_VALUE = [ALPHA, BETA, GAMMA, DELTA, RHO, PI]

def translate_letter(str):
    for i in range(0, len(LETTERS)):
        if str == LETTERS[i]:
            str == LETTERS_VALUE[i]
    return str

def replace_letters(str):
    if str is None:
        return None
    for i in range(0, len(LETTERS)):
        tes = LETTERS[i]
        test = ""
        test.find(tes)
        str = str.replace(LETTERS[i], LETTERS_VALUE[i])
        str.replace('a', 'hola')
    return str

PI_CONST = PI
PI_VALUE_CONST = math.pi

ERROR = -1

#CAMBIAR PARAM, PARAM_2... POR UN ARRAY
class Tree:
    steps = None
    parameters = []
    parameter_names = None

    def __init__(self):
        self.data = None
        self.left = None
        self.right = None
    
    def debug_print_args(self, level, space):
        if (self.data != None):
            print(space + self.data + ' | ' + str(level))
            if (self.right != None):
                self.right.debug_print_args(level + 1, space + '\t')
            if (self.left != None):
                self.left.debug_print_args(level + 1, space + '\t')
    
    def debug_print(self):
        self.debug_print_args(0, '')

    def to_string(self):
        
        #Estudiar como meter elevados y fracciones chulas (m$^3$/s)

        if (self.left is None and self.right is None):
            for i in range(0, len(LETTERS)):
                if self.data == LETTERS[i]:
                    return LETTERS_VALUE[i]
            return self.data
        if (self.data == ')'):
            return '(' + self.left.to_string() + ')'
        if (self.data == '+'):
            return self.left.to_string() + ' + ' + self.right.to_string()
        if (self.data == '-'):
            return self.left.to_string() + ' - ' + self.right.to_string()
        if (self.data == '^'):
            return self.left.to_string() + ' ^ ' + self.right.to_string()
        if (self.data == '*'):
            return self.left.to_string() + ' * ' + self.right.to_string()
        if (self.data == '/'):
            return self.left.to_string() + ' / ' + self.right.to_string()
        if (self.data == 'sin'):
            return self.data + '(' + self.left.to_string() + ')'
        if (self.data == 'cos'):
            return self.data + '(' + self.left.to_string() + ')'
        
    def initialize_tree(self, steps, parameters=None, parameter_names=None):
        self.steps = steps
        self.parameters = parameters
        self.parameter_names = parameter_names
    
    #For root with values
    def resolve_tree(self):
        return self.recursive_resolve_tree(steps=self.steps, parameters=self.parameters, parameters_names=self.parameter_names)

    def recursive_resolve_tree(self, steps, parameters, parameters_names):
        if self.data == None:
            raise TreeException('Empty node!')
        elif self.data == ')':
            rtr = self.left.recursive_resolve_tree(steps=steps, parameters=parameters, parameters_names=parameters_names)
            return rtr
        elif self.data == '+':
            return np.array([li + ri for li, ri in zip(self.left.recursive_resolve_tree(steps=steps, parameters=parameters, parameters_names=parameters_names), self.right.recursive_resolve_tree(steps=steps, parameters=parameters, parameters_names=parameters_names))])
        elif self.data == '-':
            return np.array([li - ri for li, ri in zip(self.left.recursive_resolve_tree(steps=steps, parameters=parameters, parameters_names=parameters_names), self.right.recursive_resolve_tree(steps=steps, parameters=parameters, parameters_names=parameters_names))])
        elif self.data == '/':
            #Cuidar dividir entre 0!
            try:
                test = np.array([li / ri for li, ri in zip(self.left.recursive_resolve_tree(steps=steps, parameters=parameters, parameters_names=parameters_names), self.right.recursive_resolve_tree(steps=steps, parameters=parameters, parameters_names=parameters_names))])
                return np.array([li / ri for li, ri in zip(self.left.recursive_resolve_tree(steps=steps, parameters=parameters, parameters_names=parameters_names), self.right.recursive_resolve_tree(steps=steps, parameters=parameters, parameters_names=parameters_names))])
            except ZeroDivisionError:
                #temporal
                return self.left.recursive_resolve_tree(steps=steps, parameters=parameters, parameters_names=parameters_names)
        elif self.data == '*':
            return np.array([li * ri for li, ri in zip(self.left.recursive_resolve_tree(steps=steps, parameters=parameters, parameters_names=parameters_names), self.right.recursive_resolve_tree(steps=steps, parameters=parameters, parameters_names=parameters_names))])
        elif self.data == '^':
            return np.array([pow(li, ri) for li, ri in zip(self.left.recursive_resolve_tree(steps=steps, parameters=parameters, parameters_names=parameters_names), self.right.recursive_resolve_tree(steps=steps, parameters=parameters, parameters_names=parameters_names))])
        elif self.data == parameters_names[0]:
            return parameters[0]
        elif len(parameters_names) > 1 and self.data == parameters_names[1]:
            return parameters[1]
        elif len(parameters_names) > 2 and self.data == parameters_names[2]:
            return parameters[2]
        elif self.data == 'sin':
            return np.array([math.sin(li) for li in self.left.recursive_resolve_tree(steps=steps, parameters=parameters, parameters_names=parameters_names)])
        elif self.data == 'cos':
            return np.array([math.cos(li) for li in self.left.recursive_resolve_tree(steps=steps, parameters=parameters, parameters_names=parameters_names)]) 
        elif self.data == 'sqrt':
            return np.array([math.sqrt(li) for li in self.left.recursive_resolve_tree(steps=steps, parameters=parameters, parameters_names=parameters_names)])
        #Constants
        elif self.data == PI_CONST:
            return np.linspace(PI_VALUE_CONST, PI_VALUE_CONST, steps)  
        #is a number
        else:
            return np.linspace(float(self.data), float(self.data), steps) 
               

class TreeException(Exception):
    pass

#For the tree generator
def find_nth_ocurrence(ecuation, find, ocurrence, ini):
    index = ini
    for i in range(0, ocurrence):
        tmp = ecuation[index+1:len(ecuation)]
        index += ecuation[index+1:len(ecuation)].index(find) + 1
    return index

#Returns None if the tree could not be created
def tree_generator(ecuation, param_names):
    
    if ecuation == '' or ecuation is None:
        return None

    ecuation = ecuation.replace(' ', '')
    ecuation = replace_letters(ecuation)
    ecuation = ecuation.replace('X', 'x')
    ecuation = ecuation.replace('Y', 'y')
    ecuation = ecuation.replace('Z', 'z')
    if ecuation[0] == '-':
        ecuation = '0' + ecuation

    try:
        return recursive_tree_generator(ecuation, param_names)
    except TreeException as err:
        print('Tree could not be constructed! ' + str(err))
        return None

'''
nodo.data ===
) -> left
+ -> left + right
- -> left - right
^ -> left ^ right
* -> left * right
/ -> left / right
sin -> sin(left)
cos -> cos(left)
'''
def recursive_tree_generator(ecuation, param_names):

        father = Tree()
        composite = False

        #Composite function
        if 'sin' in ecuation and ecuation.index('sin') == 0:
            father.data = 'sin'
            composite = True
            ecuation = ecuation[3: len(ecuation)]
            if (ecuation[0] != '('):
                raise TreeException('Expresion not defined. Function without () i.e. sin(...)!')
        elif 'cos' in ecuation and ecuation.index('cos') == 0:
            father.data = 'cos'
            composite = True
            ecuation = ecuation[3: len(ecuation)]
            if (ecuation[0] != '('):
                raise TreeException('Expresion not defined. Function without () i.e. sin(...)!')
        elif 'sqrt' in ecuation and ecuation.index('sqrt') == 0:
            father.data = 'sqrt'
            composite = True
            ecuation = ecuation[4: len(ecuation)]
            if (ecuation[0] != '('):
                raise TreeException('Expresion not defined. Function without () i.e. sin(...)!')
        if '(' in ecuation and ecuation.index('(') == 0:
            first_par = ecuation.index('(')
            if ')' not in ecuation:
                raise TreeException('Expresion not defined. Parenthesis not closed!')
            
            second_par = ecuation.index(')')

            #There is a parenthesis inside another
            if '(' in ecuation[first_par + 1 : second_par]:
                par_deep = ecuation[first_par + 1 : second_par - 1].count('(')
                second_par = find_nth_ocurrence(ecuation, ')', par_deep, second_par)

            compositeTree = Tree()
            compositeTree.data = father.data

            #parenthesis is the last index
            if second_par == len(ecuation) - 1:
                if (composite):
                    father.left = recursive_tree_generator(ecuation[first_par + 1 : second_par], param_names)
                    return father
                father.data = ')'
                father.left = recursive_tree_generator(ecuation[first_par + 1 : second_par], param_names)
                return father
            elif ecuation[second_par + 1] == '-':
                father.data = '-'
                if (composite):
                    compositeTree.left = recursive_tree_generator(ecuation[first_par + 1 : second_par], param_names)
                    father.left = compositeTree
                else:
                    father.left = recursive_tree_generator(ecuation[first_par + 1 : second_par], param_names)
                father.right = recursive_tree_generator(ecuation[second_par + 2: len(ecuation)], param_names)
            elif ecuation[second_par + 1] == '+':
                father.data = '+'
                if (composite):
                    compositeTree.left = recursive_tree_generator(ecuation[first_par + 1 : second_par], param_names)
                    father.left = compositeTree
                else:
                    father.left = recursive_tree_generator(ecuation[first_par + 1 : second_par], param_names)
                father.right = recursive_tree_generator(ecuation[second_par + 2: len(ecuation)], param_names)
            elif ecuation[second_par + 1] == '/':
                father.data = '/'
                if (composite):
                    compositeTree.left = recursive_tree_generator(ecuation[first_par + 1 : second_par], param_names)
                    father.left = compositeTree
                else:
                    father.left = recursive_tree_generator(ecuation[first_par + 1 : second_par], param_names)
                father.right = recursive_tree_generator(ecuation[second_par + 2: len(ecuation)], param_names)
            elif ecuation[second_par + 1] == '*':
                father.data = '*'
                if (composite):
                    compositeTree.left = recursive_tree_generator(ecuation[first_par + 1 : second_par], param_names)
                    father.left = compositeTree
                else:
                    father.left = recursive_tree_generator(ecuation[first_par + 1 : second_par], param_names)
                father.right = recursive_tree_generator(ecuation[second_par + 2: len(ecuation)], param_names)
            elif ecuation[second_par + 1] == '^':
                father.data = '^'
                if (composite):
                    compositeTree.left = recursive_tree_generator(ecuation[first_par + 1 : second_par], param_names)
                    father.left = compositeTree
                else:
                    father.left = recursive_tree_generator(ecuation[first_par + 1 : second_par], param_names)
                father.right = recursive_tree_generator(ecuation[second_par + 2: len(ecuation)], param_names)
            else:
                raise TreeException('Expresion not defined. Pathenthesis does not match!')
                return ERROR
        elif '-' in ecuation and ('(' not in ecuation or (ecuation.index('-') < ecuation.index('('))):
            split_index = ecuation.index('-')
            ec1 = ecuation[0 : split_index]
            ec2 = ecuation[split_index + 1 : len(ecuation)]
            father.left = recursive_tree_generator(ec1, param_names)
            father.right = recursive_tree_generator(ec2, param_names)
            father.data = '-'
        elif '+' in ecuation and ('(' not in ecuation or (ecuation.index('+') < ecuation.index('('))):
            split_index = ecuation.index('+')
            ec1 = ecuation[0 : split_index]
            ec2 = ecuation[split_index + 1 : len(ecuation)]
            father.left = recursive_tree_generator(ec1, param_names)
            father.right = recursive_tree_generator(ec2, param_names)
            father.data = '+'
        elif '/' in ecuation and ('(' not in ecuation or (ecuation.index('/') < ecuation.index('('))):
            split_index = ecuation.index('/')
            ec1 = ecuation[0 : split_index]
            ec2 = ecuation[split_index + 1 : len(ecuation)]
            father.left = recursive_tree_generator(ec1, param_names)
            father.right = recursive_tree_generator(ec2, param_names)
            father.data = '/'
        elif '*' in ecuation and ('(' not in ecuation or (ecuation.index('*') < ecuation.index('('))):
            split_index = ecuation.index('*')
            ec1 = ecuation[0 : split_index]
            ec2 = ecuation[split_index + 1 : len(ecuation)]
            father.left = recursive_tree_generator(ec1, param_names)
            father.right = recursive_tree_generator(ec2, param_names)
            father.data = '*'
        elif '^' in ecuation and ('(' not in ecuation or (ecuation.index('^') < ecuation.index('('))):
            split_index = ecuation.index('^')
            ec1 = ecuation[0 : split_index]
            ec2 = ecuation[split_index + 1 : len(ecuation)]
            father.left = recursive_tree_generator(ec1, param_names)
            father.right = recursive_tree_generator(ec2, param_names)
            father.data = '^'
        else:
            #Base case
            if (len(ecuation) == 0):
                raise TreeException('Expresion not defined. No operand!')
                return ERROR
            if (ecuation == param_names[0]):
                father.data = param_names[0]
            elif (len(param_names) > 1 and ecuation == param_names[1]):
                father.data = param_names[1]
            elif (len(param_names) > 2 and ecuation == param_names[2]):
                father.data = param_names[2]
            elif (ecuation == PI_CONST):
                father.data = PI_CONST
            else:
                father.data = ecuation
        
        return father

class ControlException(Exception):
    pass
            
class MyTextCtrl(wx.TextCtrl):

    def __init__(self, parent=None, placeholder=None, pos=None):
        if parent == None:
            return
        super().__init__(parent)
        self.SetHint(placeholder)
        self.Position = pos

    def getText(self):
        return self.GetValue()
        #return wx.TextCtrl.GetValue()

class MyCheckBox(wx.CheckBox):

    def __init__(self, parent=None, placeholder=None, pos=None):
        if parent == None:
            return
        super().__init__(parent)
        self.SetHint(placeholder)
        self.Position = pos

class MyButton(wx.Button):

    def __init__(self, parent=None, placeholder=None, pos=None):
        if parent == None:
            return
        super().__init__(parent)
        self.SetHint(placeholder)
        self.Position = pos

class MyComboBox(wx.ComboBox):

    def __init__(self, parent=None, placeholder=None, pos=None, choices=COLORS_USER_INTERFACE, style=wx.CB_READONLY):
        if parent == None:
            return
        super().__init__(parent, choices=choices, style=style)
        self.Position = pos
        self.Bind(wx.EVT_COMBOBOX, self.setBackgroundColour)

    ##PENDIENTE DE HACER
    def setBackgroundColour(self, event):
        #ALPHA from transparent (0) to opaque (255)
        print(colors.to_rgba('blue'))
        print(colors.to_rgba(self.GetValue()))
        colors_back_float = colors.to_rgba(self.GetValue())
        colors_back = list(map(lambda k : int(k * 255), colors_back_float))
        print(colors_back)
        #self.SetBackgroundColour(self.GetValue())
        #print(plt.pcolor(self.GetValue()).to_rgba())
        my_color = wx.Colour(colors_back[0], colors_back[1], colors_back[2], alpha=100)
        self.BackgroundColour(my_color)

class Curve():
    #Ui curve name
    curve_name_ui_edit = MyTextCtrl()

    #Text form ui edits
    curve_name = None

    #Ui text edit functions
    x_function_ui_edit = MyTextCtrl()
    y_function_ui_edit = MyTextCtrl()
    z_function_ui_edit = MyTextCtrl()

    #Text from ui edits
    x_function_text = None
    y_function_text = None
    z_function_text = None

    #Generated trees from ui functions
    x_tree = Tree()
    y_tree = Tree()
    z_tree = Tree()

    #Np arrays with values
    x = None
    y = None
    z = None

    #Color cmb
    curve_color_ui_combo = MyComboBox()

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
            self.curve_color_text = DEFAULT_CURVE_COLOR
        else:
            self.curve_color_text = COLORS_GRAPH[COLORS_USER_INTERFACE.index(self.curve_color_ui_combo.GetValue())]

    def translate(self):
        self.curve_name = replace_letters(self.curve_name)
        self.x_function_text = replace_letters(self.x_function_text)
        self.y_function_text = replace_letters(self.y_function_text)
        self.z_function_text = replace_letters(self.z_function_text)

    def create_trees(self, parameter_names):
        if self.curve_name is not None:
            self.x_tree = tree_generator(self.x_function_text, parameter_names)
            self.y_tree = tree_generator(self.y_function_text, parameter_names)
            self.z_tree = tree_generator(self.z_function_text, parameter_names)

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

class Vector():
    #Ui curve name
    vector_name_ui_edit = MyTextCtrl()

    #Text form ui edits
    vector_name = None

    #Ui text edit functions
    ini_point_ui_edit = MyTextCtrl()
    value_ui_edit = MyTextCtrl()

    #Text from ui edits
    ini_point_text = None
    value_text = None

    #Real Values
    ini_point_value = None
    value_value = None

    #Color cmb
    vector_color_ui_combo = MyComboBox()

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
            raise ControlException('Init point needs a value for vector ' + self.vector_name + '.')

        if (self.value_ui_edit.GetValue() != ''):
            self.value_text = self.value_ui_edit.GetValue()
            string = self.value_ui_edit.GetValue().replace('(', '').replace(')', '').split(',')
            self.value_value = []

            for i in range(0, len(string)):
                self.value_value.append(float(string[i]))
        else:
            raise ControlException('Value needs a value for vector ' + self.vector_name + '.')
        
        if self.vector_color_ui_combo.GetValue() == '':
            self.vector_color_text = DEFAULT_VECTOR_COLOR
        else:
            self.vector_color_text = COLORS_GRAPH[COLORS_USER_INTERFACE.index(self.vector_color_ui_combo.GetValue())]


    def translate(self):
        self.vector_name = replace_letters(self.vector_name)
        self.ini_point_text = replace_letters(self.ini_point_text)
        self.value_text = replace_letters(self.value_text)

    def clean(self):
        self.vector_name = None

        self.ini_point_text = None
        self.value_text = None

        self.ini_point_value = None
        self.value_value = None

class Parameter():

    #Ui curve name
    parameter_name_ui_edit = MyTextCtrl()

    #Text form ui edits
    parameter_name = None

    #Ui text edit functions
    lower_bound_ui_edit = MyTextCtrl()
    upper_bound_ui_edit = MyTextCtrl()

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
                raise ControlException('Expected at least one value (lower) for ' + self.parameter_name + '.')
                return False
            
            self.lower_bound_text = self.lower_bound_ui_edit.GetValue()

            aux_tree = Tree()
            aux_tree = tree_generator(self.lower_bound_text, self.parameter_name)
            aux_tree.initialize_tree(steps=1, parameter_names=[self.parameter_name])
            value_tree = aux_tree.resolve_tree()[0]
            self.value_array = np.linspace(value_tree, value_tree, steps)

        else:
            self.lower_bound_text = self.lower_bound_ui_edit.GetValue()
            self.upper_bound_text = self.upper_bound_ui_edit.GetValue()

            aux_tree = Tree()
            aux_tree = tree_generator(self.lower_bound_text, self.parameter_name)
            aux_tree.initialize_tree(steps=1, parameter_names=[self.parameter_name])
            value_tree = aux_tree.resolve_tree()[0]

            aux_tree = tree_generator(self.upper_bound_text, self.parameter_name)
            aux_tree.initialize_tree(steps=1, parameter_names=[self.parameter_name])
            value_tree_2 = aux_tree.resolve_tree()[0]

            self.value_array = np.linspace(value_tree, value_tree_2, steps)

        return True

    def translate(self):
        self.parameter_name = replace_letters(self.parameter_name)
        self.lower_bound_text = replace_letters(self.lower_bound_text)
        self.upper_bound_text = replace_letters(self.upper_bound_text)

    def clean(self):
        self.parameter_name = None

        self.lower_bound_text = None
        self.upper_bound_text = None

        self.value_array = None

class Bounds():
    #Ui text edit functions
    x_lower_bound_ui_edit = MyTextCtrl()
    y_lower_bound_ui_edit = MyTextCtrl()
    z_lower_bound_ui_edit = MyTextCtrl()
    x_upper_bound_ui_edit = MyTextCtrl()
    y_upper_bound_ui_edit = MyTextCtrl()
    z_upper_bound_ui_edit = MyTextCtrl()

    #Text from ui edits
    x_lower_bound_text = None
    y_lower_bound_text = None
    z_lower_bound_text = None
    x_upper_bound_text = None
    y_upper_bound_text = None
    z_upper_bound_text = None

    x_lower_bound_value = DEFAULT_LOWER_AXIS_BOUND
    y_lower_bound_value = DEFAULT_LOWER_AXIS_BOUND
    z_lower_bound_value = DEFAULT_LOWER_AXIS_BOUND
    x_upper_bound_value = DEFAULT_UPPER_AXIS_BOUND
    y_upper_bound_value = DEFAULT_UPPER_AXIS_BOUND
    z_upper_bound_value = DEFAULT_UPPER_AXIS_BOUND

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
        self.x_lower_bound_text = replace_letters(self.x_lower_bound_text)
        self.y_lower_bound_text = replace_letters(self.y_lower_bound_text)
        self.z_lower_bound_text = replace_letters(self.z_lower_bound_text)
        self.x_upper_bound_text = replace_letters(self.x_upper_bound_text)
        self.y_upper_bound_text = replace_letters(self.y_upper_bound_text)
        self.z_upper_bound_text = replace_letters(self.z_upper_bound_text)

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

        self.x_lower_bound_value = DEFAULT_LOWER_AXIS_BOUND
        self.y_lower_bound_value = DEFAULT_LOWER_AXIS_BOUND
        self.z_lower_bound_value = DEFAULT_LOWER_AXIS_BOUND
        self.x_upper_bound_value = DEFAULT_UPPER_AXIS_BOUND
        self.y_upper_bound_value = DEFAULT_UPPER_AXIS_BOUND
        self.z_upper_bound_value = DEFAULT_UPPER_AXIS_BOUND

        self.x_bounds = None
        self.y_bounds = None
        self.z_bounds = None

        self.plot_2d = None

class Controls(wx.App):
    
    steps_ui_edit = MyTextCtrl()
    steps_value = DEFAULT_STEPS

    plot_2d_ui_checkbox = MyCheckBox()
    plot_2d_checked = None

    plot_ui_button = MyButton()

    def initialize(self):
        if (self.steps_ui_edit.GetValue() != ''):
            self.steps_value = float(self.steps_ui_edit.GetValue())
        
        self.plot_2d_checked = self.plot_2d_ui_checkbox.IsChecked()

    def clean(self):
        self.steps_value = DEFAULT_STEPS

        self.plot_2d_checked = None

class MyFrame(wx.Frame):

    #Curves
    curves = [Curve(), Curve()]

    #Parameters
    parameters = [Parameter(), Parameter(), Parameter()]

    #Vectors
    vectors = [Vector(), Vector(), Vector()]

    #Graph bounds
    bounds = Bounds()

    #Controls
    controls = Controls()

    #Plotter for Graph
    plotter = plt

    #Sets up the user interface
    def __init__(self):
        super().__init__(parent=None, title='Curve Plotter')

        #For the row heights
        counter = 0

        #Curves
        for i in range(0, len(self.curves)):
            self.curves[i].curve_name_ui_edit = MyTextCtrl(self, 'curve name', (FIRST_COLUMN, USER_INTERFACE_MARGINS + SPACING_ROWS*counter)) 
            self.curves[i].x_function_ui_edit = MyTextCtrl(self, 'x function', (SECOND_COLUMN, USER_INTERFACE_MARGINS + SPACING_ROWS*counter))
            self.curves[i].y_function_ui_edit = MyTextCtrl(self, 'y function', (THIRD_COLUMN, USER_INTERFACE_MARGINS + SPACING_ROWS*counter))
            self.curves[i].z_function_ui_edit = MyTextCtrl(self, 'z function', (FOURTH_COLUMN, USER_INTERFACE_MARGINS + SPACING_ROWS*counter))
            self.curves[i].curve_color_ui_combo = MyComboBox(self, pos=(FIFTH_COLUMN, USER_INTERFACE_MARGINS + SPACING_ROWS*counter))
            counter += 1

        #Parameters
        for i in range(0, len(self.parameters)):
            self.parameters[i].parameter_name_ui_edit =  MyTextCtrl(self, 'parameter name', (FIRST_COLUMN, USER_INTERFACE_MARGINS + SPACING_ROWS*counter)) 
            self.parameters[i].lower_bound_ui_edit = MyTextCtrl(self, 'lower bound', (SECOND_COLUMN, USER_INTERFACE_MARGINS + SPACING_ROWS*counter))
            self.parameters[i].upper_bound_ui_edit = MyTextCtrl(self, 'upper bound', (THIRD_COLUMN, USER_INTERFACE_MARGINS + SPACING_ROWS*counter))
            counter += 1

        #Vectors
        for i in range(0, len(self.vectors)):
            self.vectors[i].vector_name_ui_edit =  MyTextCtrl(self, 'vector name', (FIRST_COLUMN, USER_INTERFACE_MARGINS + SPACING_ROWS*counter)) 
            self.vectors[i].ini_point_ui_edit = MyTextCtrl(self, 'init point', (SECOND_COLUMN, USER_INTERFACE_MARGINS + SPACING_ROWS*counter))
            self.vectors[i].value_ui_edit = MyTextCtrl(self, 'value', (THIRD_COLUMN, USER_INTERFACE_MARGINS + SPACING_ROWS*counter))
            self.vectors[i].vector_color_ui_combo = MyComboBox(self, pos=(FOURTH_COLUMN, USER_INTERFACE_MARGINS + SPACING_ROWS*counter))
            counter += 1

        #Graph Bounds
        self.bounds.x_lower_bound_ui_edit = MyTextCtrl(self, 'x graph lower bound', (FIRST_COLUMN, USER_INTERFACE_MARGINS + SPACING_ROWS*counter))
        self.bounds.y_lower_bound_ui_edit = MyTextCtrl(self, 'y graph lower bound', (SECOND_COLUMN, USER_INTERFACE_MARGINS + SPACING_ROWS*counter))
        self.bounds.z_lower_bound_ui_edit = MyTextCtrl(self, 'z graph lower bound', (THIRD_COLUMN, USER_INTERFACE_MARGINS + SPACING_ROWS*counter))
        counter += 1

        self.bounds.x_upper_bound_ui_edit = MyTextCtrl(self, 'x graph upper bound', (FIRST_COLUMN, USER_INTERFACE_MARGINS + SPACING_ROWS*counter))
        self.bounds.y_upper_bound_ui_edit = MyTextCtrl(self, 'y graph upper bound', (SECOND_COLUMN, USER_INTERFACE_MARGINS + SPACING_ROWS*counter))
        self.bounds.z_upper_bound_ui_edit = MyTextCtrl(self, 'z graph upper bound', (THIRD_COLUMN, USER_INTERFACE_MARGINS + SPACING_ROWS*counter))
        counter += 1

        #Controls
        self.controls.steps_ui_edit = MyTextCtrl(self, 'steps', (FIFTH_COLUMN, USER_INTERFACE_MARGINS + SPACING_ROWS*(counter-3)))
        self.controls.plot_2d_ui_checkbox = wx.CheckBox(self, label='2d plot', pos=(FIFTH_COLUMN + 35, USER_INTERFACE_MARGINS + SPACING_ROWS*(counter-2)))
        self.controls.plot_ui_button = wx.Button(self, label='Plot Curve', pos=(FIFTH_COLUMN + 35, USER_INTERFACE_MARGINS + SPACING_ROWS*(counter-1)))
        counter += 1

        #Bind the function with the ui click
        #Poner el bind en controls!
        self.controls.plot_ui_button.Bind(wx.EVT_BUTTON, self.OnClickButton)

        #Set the window size
        self.Size = (WIDTH, USER_INTERFACE_MARGINS + SPACING_ROWS*(counter))

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
            except ControlException as err:
                self.warning_message(str(err))
                return False
        
        #Curves
        for i in range(0, len(self.curves)):
            try:
                self.curves[i].initialize()
            except ControlException as err:
                self.warning_message(str(err))
                return False
        
        #Vectors
        for i in range(0, len(self.vectors)):
            try:
                self.vectors[i].initialize()
            except ControlException as err:
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
            self.parameter_names[i] = replace_letters(self.parameter_names[i])
        
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
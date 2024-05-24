import utility
import numpy as np
import math

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
            for i in range(0, len(utility.LETTERS)):
                if self.data == utility.LETTERS[i]:
                    return utility.LETTERS_VALUE[i]
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
        elif self.data == utility.PI_CONST:
            return np.linspace(utility.PI_VALUE_CONST, utility.PI_VALUE_CONST, steps)  
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
    ecuation = utility.replace_letters(ecuation)
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
            elif (ecuation == utility.PI_CONST):
                father.data = utility.PI_CONST
            else:
                father.data = ecuation
        
        return father

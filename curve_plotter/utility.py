import math

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

#Should be done with a configuration file
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

#Should be done with a configuration file
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


class ControlException(Exception):
    pass
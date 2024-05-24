import utility
import wx
from matplotlib import colors

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

    def __init__(self, parent=None, placeholder=None, pos=None, choices=utility.COLORS_USER_INTERFACE, style=wx.CB_READONLY):
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
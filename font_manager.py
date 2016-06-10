from random_list import RandomList
from PyQt5 import QtGui

class FontManager():
    def __init__(self, fontSize):
        self.fontSize = fontSize
        self.allFonts = QtGui.QFontDatabase().families(QtGui.QFontDatabase.Latin)
        self.randomList = RandomList(len(self.allFonts))

    def step(self):
        return self.allFonts[self.randomList.step()]
        
    def changeFontSize(self, delta):
        self.fontSize += delta

if __name__ == '__main__':
    f = FontManager()
    print(f.step())
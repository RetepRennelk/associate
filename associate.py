import sys, argparse
from argparse import RawTextHelpFormatter

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QBoxLayout

from font_manager import FontManager
from ideaz import Ideaz

class Labels():
    def __init__(self, N_labels, fontSize):
        self.fontSize = fontSize
        self.initLabels(N_labels)
        self.fontManager = FontManager(fontSize)

    def stepFont(self):
        for label in self.labels:
            newFont = QtGui.QFont(self.fontManager.step(), self.fontManager.fontSize)
            label.setFont(newFont)

    def changeFontSize(self, delta):
        self.fontManager.changeFontSize(delta)
        for label in self.labels:
            font = label.font()
            font.setPointSize(self.fontManager.fontSize)
            label.setFont(font)

    def initLabels(self, N_labels):
        self.labels = []
        self.N_labels = N_labels
        for i in range(N_labels):
            self.labels.append(QLabel(""))
            self.labels[-1].setAlignment(Qt.AlignCenter)

    def setText(self, string_list):
        for i, s in enumerate(string_list):
            self.labels[i].setText(s)

class HV(QWidget):
    def __init__(self, labels):
        QWidget.__init__(self)
        self.labels = labels
        self.layout =  QBoxLayout(QBoxLayout.LeftToRight)
        for label in labels.labels:
            self.layout.addWidget(label)
        self.setLayout(self.layout)

    def setLabels(self, labels):
        for label in self.labels.labels:
            self.layout.removeWidget(label)
            label.setParent(None)
        self.labels = labels
        for label in labels.labels:
            self.layout.addWidget(label)

    def setLeftToRight(self):
        self.layout.setDirection(QtWidgets.QBoxLayout.LeftToRight)

    def setTopToBottom(self):
        self.layout.setDirection(QtWidgets.QBoxLayout.TopToBottom)

class SampleWindow(QWidget):
    def __init__(self, ideaz):
        QWidget.__init__(self)
        self.setGeometry(300, 300, 250, 175)
        self.setWindowTitle("Associate")
        self.ideaz = ideaz

        fontSize = 20
        N_layers = ideaz.getNrOfLayers()
        self.labels = Labels(N_layers, fontSize)
        self.labels.setText(ideaz.step())
        self.labels.stepFont()

        self.hv = HV(self.labels)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.hv)

        self.setLayout(layout)

    def keyPressEvent(self, e):
        if e.key()>=Qt.Key_0 and e.key()<=Qt.Key_9:
            N_layers = e.key() - 48
            self.ideaz.setList(N_layers)
            newLabels = Labels(self.ideaz.getNrOfLayers(), 20);
            self.hv.setLabels(newLabels)
            self.labels = newLabels

        if e.text() == 'h':
            self.hv.setLeftToRight()
        elif e.text() == 'v':
            self.hv.setTopToBottom()
        elif e.text( ) == '+':
            self.labels.changeFontSize(+1)
        elif e.text( ) == '-':
            self.labels.changeFontSize(-1)

        if e.text() not in ['+', '-', 'h', 'v']:
            self.labels.stepFont()
            self.labels.setText(ideaz.step())

if __name__ == '__main__':
    try:
        myApp = QApplication(sys.argv)
    except:
        myApp = QApplication.instance()

    descr = 'associate.py'
    parser = argparse.ArgumentParser(description=descr, formatter_class=RawTextHelpFormatter)
    parser.add_argument('filename', nargs='+', type=str, help='file name')
    parser.add_argument('-N_layers', nargs='?', type=int, default=0)
    args = parser.parse_args()

    ideaz = Ideaz(args.filename, args.N_layers)
    myWindow = SampleWindow(ideaz)
    myWindow.show()
    myApp.exec_()
    sys.exit()

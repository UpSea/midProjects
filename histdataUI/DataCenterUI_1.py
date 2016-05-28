import os,sys
from PyQt4 import QtGui,QtCore

from Layouts.dataManagerLayout import dataManagerLayout
from Layouts.dataVisualizerLayout import dataVisualizerLayout

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        cw = QtGui.QWidget()
        self.setCentralWidget(cw)
        mainlayout = QtGui.QVBoxLayout()
        cw.setLayout(mainlayout) 
        
        
        mainlayout.addLayout(dataManagerLayout(self))
        mainlayout.addLayout(dataVisualizerLayout(self))
        mainlayout.setStretch(0,1)
        mainlayout.setStretch(1,2)

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.showMaximized()
    sys.exit(app.exec_())
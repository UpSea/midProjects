#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        self.btn = QPushButton('Button', self)
        self.btn.resize(self.btn.sizeHint())

        self.lb = QLabel('...',self)

        #create the 5x5 table...
        self.table = QTableWidget(5,5,self)
        '''
        map(lambda (row,col): self.createCheckItem(self.table, row, col),
            [(row, col) for row in range(0, 5) for col in range(0, 5)])
        
        
        '''

        vbox = QVBoxLayout()
        vbox.addWidget(self.btn)
        vbox.addWidget(self.lb)
        vbox.addWidget(self.table)
        self.setLayout(vbox)  

        #...and connect our signal handler to the cellChanged(int, int) signal
        QObject.connect(self.table, SIGNAL("cellChanged(int, int)"), self.myCellChanged)

        self.setGeometry(300, 300, 600, 300)
        self.setWindowTitle('nothing...')   
        self.show()

    #signal handler
    def myCellChanged(self,row, col):
        #print row, col
        #print self.table.currentItem().text()
        self.lb.setText(self.table.currentItem().text())

    #just a helper function to setup the table
    def createCheckItem(self,table, row, col):
        check = QTableWidgetItem("Test")
        check.setCheckState(Qt.Checked)
        table.setItem(row,col,check)

def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
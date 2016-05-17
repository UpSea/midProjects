# -*- coding: utf-8 -*-
from PyQt4 import QtGui
import sys
from MainFrame import MainFrame

if __name__ == '__main__':
    qApp=QtGui.QApplication(sys.argv)
    main=MainFrame()
    main.showMaximized()
    sys.exit(qApp.exec_())


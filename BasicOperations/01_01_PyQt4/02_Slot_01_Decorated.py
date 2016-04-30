from PyQt4 import QtGui, QtCore

class MainWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        btn = QtGui.QPushButton(u"点我", self)
        self.connect(btn, QtCore.SIGNAL("clicked()"), self,
                     QtCore.SLOT("onClicked()"))
    @QtCore.pyqtSlot()
    def onClicked(self):
        QtGui.QMessageBox.information(self, u"信息", u"由槽弹出")
app = QtGui.QApplication([])
m = MainWidget()
m.show()
app.exec_()
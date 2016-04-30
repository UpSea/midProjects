from PyQt4 import QtGui, QtCore
class MyButton(QtGui.QPushButton):
    def __init__(self, _id, *args, **kwargs):
        self._id = _id
        QtGui.QPushButton.__init__(self, *args, **kwargs)
        self.connect(self, QtCore.SIGNAL("clicked()"), self.emitClicked)
    def emitClicked(self):
        self.emit(QtCore.SIGNAL("myclicked(int)"), self._id)
app = QtGui.QApplication([])
w = QtGui.QWidget()
w.resize(100, 100)
def showMsg(_id):
    QtGui.QMessageBox.information(w, u"信息", u"查看 %d" % _id)
btn = MyButton(1, u"查看1", w)
w.connect(btn, QtCore.SIGNAL("myclicked(int)"), showMsg)
btn2 = MyButton(2, u"查看2", w)
btn2.move(0, 30)
w.connect(btn2, QtCore.SIGNAL("myclicked(int)"), showMsg)
w.show()
app.exec_()
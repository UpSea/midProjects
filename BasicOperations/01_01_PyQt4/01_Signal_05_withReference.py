'''
显式绑定slot函数
'''
from PyQt4 import QtGui, QtCore
class MyButton(QtGui.QPushButton):
    myclicked = QtCore.pyqtSignal(int)                      # 1）定义一个带 int 参数的信号
    def __init__(self, _id, *args, **kwargs):
        QtGui.QPushButton.__init__(self, *args, **kwargs)
        self._id = _id
        self.connect(self, QtCore.SIGNAL("clicked()"), self.emitMyclicked)
    def emitMyclicked(self):
        self.myclicked.emit(self._id)                       # 2）通过点击按钮触发的函数释放带 int 参数的信号
def showMsg(_id):
    QtGui.QMessageBox.information(w, u"信息", u"查看 %d" % _id) 
    
app = QtGui.QApplication([])
w = QtGui.QWidget()
w.resize(100, 100)

btn = MyButton(1, u"查看1", w)
w.connect(btn, QtCore.SIGNAL("myclicked(int)"), showMsg)    # 3）将带参数的信号与带参数的槽连接起来

btn2 = MyButton(2, u"查看2", w)
btn2.move(0, 30)
w.connect(btn2, QtCore.SIGNAL("myclicked(int)"), showMsg)

w.show()
app.exec_()
from PyQt4 import QtGui,QtCore
class MyWidget(QtGui.QWidget):  
    def __init__(self,parent=None):  
        super(MyWidget,self).__init__(parent)  
        self.resize(1000,1000)  
        #self.setStyleSheet(QString.fromLatin1("background:black"))  
        layout = QtGui.QHBoxLayout()  
        self.btn1 = QtGui.QPushButton()  
        self.btn2 = QtGui.QPushButton()  
        self.btn3 = QtGui.QPushButton()  
        layout.addWidget(self.btn1)  
        layout.addWidget(self.btn2)  
        layout.addWidget(self.btn3)  
        self.setLayout(layout)  

    def keyPressEvent(self, event):  
        keyEvent = QtGui.QKeyEvent(event)  
        #if event.key() == QtCore.Qt.Key_Escape:
        if event.key() == QtCore.Qt.Key_Enter:  
            self.focusNextChild()  
            print('adfadf')

if __name__ == "__main__":  
    import sys  
    app = QtGui.QApplication(sys.argv)  
    #MainWidget = QWidget()  
    #MainWidget.resize(800,600)  
    #childWidget = MyWidget(MainWidget)  
    childWidget = MyWidget()  
    #MainWidget.show()  
    childWidget.show()  
    app.exec_()  
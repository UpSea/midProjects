import sys  
from PyQt4.QtCore import *  
from PyQt4.QtGui import *  
class MyWidget(QWidget):  
    OnClicked = pyqtSignal([int,int],[int,str])  
    def __init__(self, parent=None):  
        super(MyWidget,self).__init__(parent)  
    def mousePressEvent(self, event):  
        if event.button() == Qt.LeftButton:  
            self.OnClicked.emit(event.x(),event.y())  
            event.accept()  
        elif event.button() == Qt.RightButton:  
            self.OnClicked[int,str].emit(event.x(),str(event.y()))  
            event.accept()  
        else:  
            super(MyWidget,self).mousePressEvent(self, event)  

def OnValueChanged_int(x,y):  
    print("左键(%d,%d)" % (x,y))  

def OnValueChanged_string(szX,szY):  
    print('右键(' + str(szX) + ',' + szY + ')')  

app = QApplication(sys.argv)   
widget = MyWidget()   
widget.show()   
widget.OnClicked.connect(OnValueChanged_int,Qt.QueuedConnection)  
widget.OnClicked[int,str].connect(OnValueChanged_string,Qt.QueuedConnection)  
sys.exit(app.exec_())
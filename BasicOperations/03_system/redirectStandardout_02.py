'''
隐式绑定slot函数
还没搞清楚这个是如何传入slot函数并绑定的
信号和槽函数名称是一样的，也没搞清是个什么机制
当是个黑盒用即可：
	1.定义slot处理函数
	2.将此函数传入构造函数即可
'''
from PyQt4 import QtCore,QtGui
import sys
class EmittingStream(QtCore.QObject):
    slotFunction = QtCore.pyqtSignal(str)                                        # 1）定义一个带 str 参数的信号
    i=0
    def write(self, text):
        if(text == '\n'):
            self.slotFunction.emit(str(text))                                    # 2）通过 print 触发的函数释放带 str 参数的信号
        else:
            self.slotFunction.emit(str(self.i) + ':' + str(text))
            self.i= self.i+1
class MainFrame(QtGui.QDialog):  
    def __init__(self):  
        super(MainFrame,self).__init__()  
        sys.stdout = EmittingStream(slotFunction=self.normalOutputWritten)       # 3）参数方式传入一个slot函数
        sys.stder = EmittingStream(slotFunction=self.normalOutputWritten)
        
        self.textEdit = QtGui.QTextEdit(self)    
        
        self.myButton = QtGui.QPushButton(self)  
        self.myButton.setObjectName("myButton")  
        self.myButton.setText("Test")  
        self.myButton.clicked.connect(self.msg)  
        
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)     
        layout.addWidget(self.myButton)
        layout.addWidget(self.textEdit)        
    def __del__(self):
        # Restore sys.stdout
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__          
    def msg(self):  
        print('test button clicked.     ')    
    def normalOutputWritten(self, text):
        """Append text to the QTextEdit."""
        # Maybe QTextEdit.append() works as well, but this is how I do it:
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()
if __name__=="__main__":    
    qApp=QtGui.QApplication(sys.argv)
    main=MainFrame()
    main.show()
    sys.exit(qApp.exec_())
    
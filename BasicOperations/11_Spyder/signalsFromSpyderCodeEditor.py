from PyQt4 import QtGui,QtCore
from spyderlib.widgets.sourcecode.codeeditor import CodeEditor

class MyWidget(QtGui.QWidget):  
    def __init__(self,parent=None):  
        super(MyWidget,self).__init__(parent)  
        self.resize(1000,1000)  
        layout = QtGui.QVBoxLayout()  
        
        editor = CodeEditor(self)
        
        self.connect(editor, QtCore.SIGNAL('modificationChanged(bool)'),
                     lambda state: self.modification_changed(state,editor_id=id(editor)))   
        self.index = 0
        self.btn1 = QtGui.QPushButton()  

        layout.addWidget(self.btn1)  

        layout.addWidget(editor)
        self.setLayout(layout) 
    def modification_changed(self, state=None, index=None, editor_id=None):
        """
        Current editor's modification state has changed
        --> change tab title depending on new modification state
        --> enable/disable save/save all actions
        """
        self.index = self.index+1
        self.btn1.setText(str(self.index)+':'+str(state))
if __name__ == "__main__":  
    import sys  
    app = QtGui.QApplication(sys.argv)  
 
    childWidget = MyWidget()   
    childWidget.show()  
    
    app.exec_()  
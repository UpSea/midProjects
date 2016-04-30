from PyQt4 import QtCore,QtGui
import sys
class StdOutRedirector:
    def __init__(self,edit):
        self.buff=''
        self.edit = edit
        self.__console__=sys.stdout
    def write(self, output_stream):
        self.buff+=output_stream
        self.edit.setText(self.buff)
class MainFrame(QtGui.QDialog):  
    def __init__(self):  
        super(MainFrame,self).__init__()  

        self.textEdit = QtGui.QTextEdit(self)    
        r_obj=StdOutRedirector(self.textEdit)
        sys.stdout=r_obj  
        sys.stderr=r_obj   
        
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
        print('test button clicked.')    
if __name__=="__main__":    
    qApp=QtGui.QApplication(sys.argv)
    main=MainFrame()
    main.show()
    sys.exit(qApp.exec_())
    
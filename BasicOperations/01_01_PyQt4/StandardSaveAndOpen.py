from PyQt4 import QtGui,QtCore
import os
#from PyQt4.QtWidgets import QFileDialog  
class MyWindow(QtGui.QWidget):  
    def __init__(self):  
        super(MyWindow,self).__init__()  
        self.myButton = QtGui.QPushButton(self)  
        self.myButton.setObjectName("myButton")  
        self.myButton.setText("Test")  
        self.myButton.clicked.connect(self.msg)  

    def msg(self):  
        #directory1 = QtGui.QFileDialog.getExistingDirectory(self,"选取文件夹",os.getcwd())   #起始路径  
        #print(directory1)  
        #fileName1 = QtGui.QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(), "All Files (*);;Text Files (*.txt)")   #设置文件扩展名过滤,注意用双分号间隔  
        #print(fileName1)  
        #files= QtGui.QFileDialog.getOpenFileNames(self,"多文件选择",os.getcwd(),  "All Files (*);;Text Files (*.txt)")  
        #print(files)  
        fileName2 = QtGui.QFileDialog.getSaveFileName(self, "文件保存", os.getcwd(),"All Files (*);;Text Files (*.txt)")  
        print(fileName2)
if __name__=="__main__":    
    import sys    

    app=QtGui.QApplication(sys.argv)    
    myshow=MyWindow()  
    myshow.show()  
    sys.exit(app.exec_())   
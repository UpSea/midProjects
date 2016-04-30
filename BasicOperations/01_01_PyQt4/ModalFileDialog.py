import sys,os
from PyQt4 import QtGui,QtCore

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    
    urls = []
    urls.append(QtCore.QUrl.fromLocalFile(os.getcwd()+'/Strategies'))
    urls.append(QtCore.QUrl.fromLocalFile(os.getcwd()))

    dialog = QtGui.QFileDialog()
    a = dialog.sidebarUrls()
    
    dialog.setSidebarUrls(urls);
    dialog.setFileMode(QtGui.QFileDialog.AnyFile);
    if(dialog.exec()):
        i = 8
    else:
        i=10
    
    app.exec_()
from PyQt4.QtGui import QApplication, QWidget, QFont, QVBoxLayout, QLineEdit
from spyderlib.widgets.internalshell import InternalShell

class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.shell = InternalShell(self, {"demo":self}, 
            multithreaded = False,
            max_line_count = 3000,
            font = QFont("Courier new", 10),
            message='mid caoni ma'
        )
        self.line_edit = QLineEdit()  
        vbox = QVBoxLayout()
        vbox.addWidget(self.line_edit)
        vbox.addWidget(self.shell)
        self.setLayout(vbox)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
    
'''
follow order will set lineEdit.
demo.line_edit.setText('fuck you.')
'''
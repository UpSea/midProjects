#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore

class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()
    def initUI(self): 

        self.lbl = QtGui.QLabel('Ubuntu', self)
        self.lbl.move(50, 150)

        # 创建组合框并添加5个候选项
        combo = QtGui.QComboBox(self)
        combo.addItem('Ubuntu')
        combo.addItem('Mandriva')
        combo.addItem('Fedora')
        combo.addItem('Red Hat')
        combo.addItem('Gentoo')

        combo.move(50, 50)

        # 当选择条目时，调用onActivate()方法
        combo.activated[str].connect(self.onActivate)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('ComboBox')
        self.show()

    def onActivate(self, text):
        # 显示文本内容，并根据文本长度调整标签控件的大小
        self.lbl.setText(text)
        self.lbl.adjustSize()

def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
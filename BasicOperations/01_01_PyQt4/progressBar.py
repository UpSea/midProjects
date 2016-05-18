#!/usr/bin/python
# -*- coding: utf-8 -*-
#http://blog.csdn.net/Kai_gai/article/details/49590323
import sys
from PyQt4 import QtGui, QtCore

class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        # 创建进度条
        self.pbar = QtGui.QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)

        self.btn = QtGui.QPushButton('Start', self)
        self.btn.move(40, 80)
        self.btn.clicked.connect(self.doAction)

        # 采用定时器激活进度条
        self.timer = QtCore.QBasicTimer()
        self.step = 0

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Progress Bar')
        self.show()

    # 每个QtCore.QObject对象及其子类都有一个timeEvent()的事件处理程序
    # 为了响应定时器，需要重新实现事件处理程序
    def timerEvent(self, e):

        if self.step >= 100:

            self.timer.stop()
            self.btn.setText('Finished')
            return

        self.step = self.step + 1
        self.pbar.setValue(self.step)

    # 启动或停止定时器
    def doAction(self):

        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('Start')
        else:
            # 通过start()方法启动定时器，该方法有两个参数：超时时间
            # 和接收事件的对象
            self.timer.start(100, self)
            self.btn.setText('Stop')


def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
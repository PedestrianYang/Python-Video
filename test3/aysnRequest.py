#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
import time

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import sys



class Singleaaa(QObject):
    aaaa = Signal(int)
    def __init__(self):
        QObject.__init__(self)

    def corubmmite(self):
        # self.aaaa.emit(1)
        for i in range(100):
            time.sleep(5)
        self.aaaa.emit(i)

class TimeThread(QThread):
    signal_time = Signal(int) # 信号

    def __init__(self, parent=None):
        super(TimeThread, self).__init__(parent)
        self.working = True
        self.num = 0

    def start_timer(self):

        self.start()

    def run(self):
        while self.working:

            self.signal_time.emit(self.num) # 发送信号
            self.num += 1
            self.sleep(1)



class MainUi(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.resize(100,100)
        self.setWindowTitle("测试测试")
        self.setContainer()


    def setContainer(self):
        b_box = QVBoxLayout()
        h_boc = QHBoxLayout()
        for i in range(5):
            lab1 = QLabel(str(i))
            lab1.installEventFilter(self)
            h_boc.addWidget(lab1)
        self.conntainerView = QVBoxLayout()

        b_box.addLayout(h_boc)
        b_box.addLayout(self.conntainerView)
        self.setLayout(b_box)


    def eventFilter(self, view, event):
        if event.type() == QEvent.MouseButtonPress:
            print("1")
            self.timer_t = TimeThread()
            self.timer_t.signal_time.connect(self.addAllView)
            self.timer_t.start()


    def addAllView(self, j):
        print("1")
        labe = QLabel()
        labe.setText(str(j))
        self.conntainerView.addWidget(labe)
        # for i in range(100):
        #     labe = QLabel()
        #     labe.setText("!111")
        #     self.conntainerView.addWidget(labe)
        #     QApplication.processEvents()

class Custom(QWidget):
    def __init__(self, a, b, c, d):
        QWidget.__init__(self)
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.setContainer()

    def setContainer(self):
        v_box = QHBoxLayout()
        lab1 = QLabel(self.a)
        lab2 = QLabel(self.b)
        lab3 = QLabel(self.c)
        lab4 = QLabel(self.d)
        v_box.addWidget(lab1)
        v_box.addWidget(lab2)
        v_box.addWidget(lab3)
        v_box.addWidget(lab4)
        self.setLayout(v_box)

    def mousePressEvent(self, view):
        print(self.a)

class MainWindos(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setContainer()

    def setContainer(self):
        v_box = QVBoxLayout()



        listView = QListWidget()

        for i in range(10):
            item = Custom(str(i), str(i+5), str(i+2), str(i+4),)
            tempItem = QListWidgetItem()
            tempItem.setSizeHint(item.sizeHint())
            listView.addItem(tempItem)
            listView.setItemWidget(tempItem, item)


        v_box.addWidget(listView)
        self.setLayout(v_box)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainUi = MainWindos()
    mainUi.show()

    app.exit(app.exec_())
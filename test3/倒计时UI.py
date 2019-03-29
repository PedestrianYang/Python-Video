from PySide2.QtWidgets import *
from PySide2.QtCore import *
import itchat
import sys
import datetime
import time
import threading

class MyTimer(QTimer):
    def __init__(self, label):
        QTimer.__init__(self)
        self.label = label


class MyUi(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("倒计时")
        self.resize(300, 200)
        self.setContainer()
        self.timers = []

    def setContainer(self):
        contaioner = QVBoxLayout()

        layout1 = QHBoxLayout()
        lab1 = QLabel('设置定时时间')
        self.input1 = QLineEdit()
        layout1.addWidget(lab1)
        layout1.addWidget(self.input1)
        contaioner.addLayout(layout1)

        self.layout2 = QVBoxLayout()
        contaioner.addLayout(self.layout2)

        commitBtn = QPushButton('开始')
        commitBtn.clicked.connect(self.btnClick)
        contaioner.addWidget(commitBtn)

        self.setLayout(contaioner)

    def btnClick(self):
        timeLab = QLabel(self.input1.text())
        self.layout2.addWidget(timeLab)

        #设置多线程时，target=方法名，如果需要穿参数不可以添加()，否则不为子线程
        thread = threading.Thread(target=self.forCountDown, name="aaaa",args=(timeLab,))
        thread.start()


    def forCountDown(self, timeLab):
        print(threading.current_thread().getName())
        count = int(timeLab.text())
        print(count)
        while count > 0:
            count -= 1
            time.sleep(1)
            timeLab.setText(str(count))

    def startTimerForCountDown(self, timeLab):
        timer = MyTimer(timeLab)
        timer.connect(self.countDown)
        timer.start(1000)

    def countDown(self, timeaaa):
        print(timeaaa)
        count = int(timeaaa.label.text())
        print(count)
        if count == 0:
            timeaaa.stop()
            return
        count -= 1
        timeaaa.label.setText(str(count))

    def run(self):
        self.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myui = MyUi()
    myui.run()
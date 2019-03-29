paht = '/Users/iyunshu/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/230b77a27d787411f138d9276629063a/Message/MessageTemp/64079042df0d216e2a61bccb3202000d/Video/1553318839336719.mp4'
import cv2
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import sys
import time
import os.path
import requests

from contextlib import closing

import ssl

class MyThread(QThread):
    singal = Signal(float)
    complete = Signal()
    def __init__(self, videoCapture):
        QThread.__init__(self)
        self.videoCapture = videoCapture
        self.fps = self.videoCapture.get(cv2.CAP_PROP_FPS)
        self.fps_num = self.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
        self.isPlay = True
        self.isRun = True



    def run(self):
        success, frame = self.videoCapture.read()
        count = 0
        while success and self.isRun:
            count += 1
            cv2.imwrite('asd.jpg', frame)
            # self.videoWriter.write(frame) #写视频帧
            time.sleep(1/self.fps)
            pixmap = QPixmap()
            pixmap.load('asd.jpg')
            # size = QSize(int(self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            #          int(self.videoCapture.get(cv2.cv2.CAP_PROP_FRAME_HEIGHT)))
            size = QSize(50,50)
            self.pixmap = pixmap.scaled(size)
            if self.isPlay:
                self.singal.emit(count / self.fps_num)
                success, frame = self.videoCapture.read() #获取下一帧
            else:
                success = True
        self.complete.emit()


class VideoPlayer(QWidget):
    def __init__(self, playPath):
        QWidget.__init__(self)
        self.playPath = playPath

        self.initPayer()
        v_box = QVBoxLayout()
        self.setContentsMargins(0,0,0,0)
        self.setLayout(v_box)



        self.labe = QLabel()
        v_box.addWidget(self.labe)

        self.progressBar = QProgressBar()

        v_box.addWidget(self.progressBar)

        self.timeLab = QLabel()


        v_box.addWidget(self.timeLab)

        h_box = QHBoxLayout()
        stopBtn = QPushButton('播放')
        stopBtn.clicked.connect(self.stopBtnClick)
        h_box.addWidget(stopBtn)

        closeBtn = QPushButton('关闭')
        closeBtn.clicked.connect(self.closeBtnClick)
        h_box.addWidget(closeBtn)

        v_box.addLayout(h_box)

        self.thread = MyThread(self.videoCapture)
        self.thread.start()
        self.thread.singal.connect(self.thresetContainer)
        self.thread.complete.connect(self.deleteThread)

        self.timeLab.setText('0:0:0/' + self.amutnTimeFormt)
        # self.progressBar.setFixedSize(int(self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)), 8)
        self.progressBar.setFixedSize(50, 8)

    def initPayer(self):
        self.videoCapture = cv2.VideoCapture(self.playPath)
        self.fps_num = self.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
        self.fps = self.videoCapture.get(cv2.CAP_PROP_FPS)
        self.fps_num = self.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
        self.timeAmount = self.fps_num / self.fps
        m, s = divmod(self.timeAmount, 60)
        h, m = divmod(m, 60)
        self.amutnTimeFormt = "%02d:%02d:%02d" % (h, m, s)
        print ("%02d:%02d:%02d" % (h, m, s))


    def stopBtnClick(self):
        if self.thread != None:
            if self.thread.isPlay:
                self.thread.isPlay = False
            else:
                self.thread.isPlay = True
        else:
            self.initPayer()
            self.thread = MyThread(self.videoCapture)
            self.thread.start()
            self.thread.singal.connect(self.thresetContainer)
            self.thread.complete.connect(self.deleteThread)

    def closeBtnClick(self):
        print(self.thread)
        if self.thread != None:
            self.thread.isRun = False


    def deleteThread(self):
        self.thread.videoCapture.release()
        self.thread.deleteLater()
        self.thread = None


    def thresetContainer(self, progress):

        currntTime = self.timeAmount * progress
        m, s = divmod(currntTime, 60)
        h, m = divmod(m, 60)
        currntTimeFormt = "%02d:%02d:%02d" % (h, m, s)
        self.timeLab.setText(currntTimeFormt+ '/' + self.amutnTimeFormt)

        self.labe.setPixmap(self.thread.pixmap)
        self.progressBar.setValue(progress * 100)


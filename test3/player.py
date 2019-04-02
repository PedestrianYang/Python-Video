paht = '/Users/iyunshu/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/230b77a27d787411f138d9276629063a/Message/MessageTemp/64079042df0d216e2a61bccb3202000d/Video/1553318839336719.mp4'
videopaa = 'https://fuli.zuida-youku-le.com/20180626/28918_0b931ffd/index.m3u8'
videopaaasdsa = '/Users/iyunshu/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/230b77a27d787411f138d9276629063a/Message/MessageTemp/02bec6574fe5da0358bfdcc0926329e0/Video/1554170899810201.mp4'
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

ssl._create_default_https_context = ssl._create_unverified_context
class DownloadMyThread(QThread):
    singal = Signal(float)
    complete = Signal()
    def __init__(self, video, videoWriter):
        QThread.__init__(self)
        self.videoCapture = video
        self.videoWriter = videoWriter
        self.videoFrames = []


    def run(self):

        self.fps = self.videoCapture.get(cv2.CAP_PROP_FPS)
        self.fps_num = self.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
        success, frame = self.videoCapture.read()
        count = 0
        while success:

            if self.videoWriter.isOpened() == False:
                self.videoWriter.open(self.videPath, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), self.fps, self.size)
            self.videoWriter.write(frame) #写视频帧
            if count > 0 and (count % (int(self.fps) * 10)) == 0:
                self.videoWriter.release()
                self.videPath = 'oto_other.mp4'

            self.videoWriter.write(frame)
            count += 1
            self.singal.emit(count / self.fps_num)
            success, frame = self.videoCapture.read()

        self.complete.emit()


class MyThread(QThread):
    singal = Signal(float)
    complete = Signal()
    def __init__(self, videoCapture, fps):
        QThread.__init__(self)
        self.videoCapture = videoCapture
        self.fps = fps
        self.isPlay = True
        self.isRun = True
        self.shouldUpdateProgress = False
        self.pos_fps = 0
        self.count = 0

    def run(self):

        while self.isRun:

            if self.shouldUpdateProgress:
                print("跳帧")
                self.shouldUpdateProgress = False
                self.count = self.pos_fps
                self.singal.emit(self.count)
                self.videoCapture.set(cv2.CAP_PROP_POS_FRAMES, self.pos_fps)

            ret, frame = self.videoCapture.read()
            time.sleep(1 / self.fps)

            cv2.imwrite('asd.jpg', frame)
            pixmap = QPixmap()
            pixmap.load('asd.jpg')

            size = QSize(int(self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)/2),
                     int(self.videoCapture.get(cv2.cv2.CAP_PROP_FRAME_HEIGHT))/2)

            self.pixmap = pixmap.scaled(size)
            self.count += 1

            self.singal.emit(self.count)
        self.complete.emit()


class VideoPlayer(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.isSliding = False
        self.slidvalue = 0

        self.initViedoPayer()

        v_box = QVBoxLayout()
        self.setContentsMargins(0,0,0,0)
        self.setLayout(v_box)

        self.labe = QLabel()
        v_box.addWidget(self.labe)

        self.progressBar = QSlider(Qt.Horizontal)
        self.progressBar.setFixedSize(int(self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)) / 2, 20)
        self.progressBar.setRange(0,99)

        self.progressBar.sliderMoved.connect(self.progressBarValueChange)
        self.progressBar.sliderReleased.connect(self.valueChangeComplete)
        v_box.addWidget(self.progressBar)

        self.timeLab = QLabel()

        self.timeAmount = self.fps_num / self.fps

        m, s = divmod(self.timeAmount, 60)
        h, m = divmod(m, 60)
        self.amutnTimeFormt = "%02d:%02d:%02d" % (h, m, s)
        print ("%02d:%02d:%02d" % (h, m, s))
        self.timeLab.setText('0:0:0/' + self.amutnTimeFormt)
        v_box.addWidget(self.timeLab)

        h_box = QHBoxLayout()
        stopBtn = QPushButton('播放')
        stopBtn.clicked.connect(self.stopBtnClick)
        h_box.addWidget(stopBtn)

        closeBtn = QPushButton('关闭')
        closeBtn.clicked.connect(self.closeBtnClick)
        h_box.addWidget(closeBtn)

        v_box.addLayout(h_box)

        self.threadqqq = MyThread(self.videoCapture,self.fps)
        self.threadqqq.start()
        self.threadqqq.singal.connect(self.thresetContainer)
        self.threadqqq.complete.connect(self.deleteThread)

    def progressBarValueChange(self, vaule):
        print('progressBarValueChange')
        self.isSliding = True
        self.slidvalue = vaule
        progress = self.slidvalue / 100 * self.fps_num
        currntTime = self.timeAmount * (progress / self.fps_num)
        m, s = divmod(currntTime, 60)
        h, m = divmod(m, 60)
        currntTimeFormt = "%02d:%02d:%02d" % (h, m, s)
        self.timeLab.setText(currntTimeFormt+ '/' + self.amutnTimeFormt)

    def valueChangeComplete(self):

        self.isSliding = False
        pos_fps = self.slidvalue / 100 * self.fps_num
        self.threadqqq.pos_fps = pos_fps
        self.threadqqq.shouldUpdateProgress = True
        print("valueChangeComplete")
        # self.videoCapture.set(cv2.CAP_PROP_POS_FRAMES, pos_fps)

    def starDownload(self, progress):
        if progress > 0.02 and self.threadqqq.isRunning() == False:
            print('开始播放')
            self.threadqqq.start()

    def downloadComplete(self):
        print('asdasd')


    def initViedoPayer(self):
        #获得视频的格式
        self.videoCapture = cv2.VideoCapture(videopaa)

        #获得码率及尺寸
        self.fps = self.videoCapture.get(cv2.CAP_PROP_FPS)
        self.fps_num = self.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)

        size = (int(self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.videoCapture.get(cv2.cv2.CAP_PROP_FRAME_HEIGHT)))



        #指定写视频的格式, I420-avi, MJPG-mp4
        self.videoWriter = cv2.VideoWriter('oto_other.mp4', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), self.fps, size)

    def stopBtnClick(self):

        if self.threadqqq != None:
            if self.threadqqq.isRunning():
                self.threadqqq.terminate()
            else:
                self.threadqqq.start()
        else:

            self.initViedoPayer()
            self.threadqqq = MyThread(self.videoCapture,self.fps)
            self.threadqqq.start()
            self.threadqqq.singal.connect(self.thresetContainer)
            self.threadqqq.complete.connect(self.deleteThread)

    def closeBtnClick(self):
        print(self.threadqqq)
        if self.threadqqq != None:
            self.threadqqq.isRun = False


    def deleteThread(self):

        print("delete")
        self.threadqqq.deleteLater()
        self.threadqqq = None
        print()


    def thresetContainer(self, progress):
        if self.isSliding == False:
            currntTime = self.timeAmount * (progress / self.fps_num)
            m, s = divmod(currntTime, 60)
            h, m = divmod(m, 60)
            currntTimeFormt = "%02d:%02d:%02d" % (h, m, s)
            self.timeLab.setText(currntTimeFormt+ '/' + self.amutnTimeFormt)

            self.labe.setPixmap(self.threadqqq.pixmap)

            self.progressBar.setValue((progress / self.fps_num) * 100)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = VideoPlayer()
    ui.show()
    sys.exit(app.exec_())
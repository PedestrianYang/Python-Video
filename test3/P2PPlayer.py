paht = '/Users/iyunshu/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/230b77a27d787411f138d9276629063a/Message/MessageTemp/64079042df0d216e2a61bccb3202000d/Video/1553318839336719.mp4'
videopaa = 'https://fuli.zuida-youku-le.com/20180626/28918_0b931ffd/index.m3u8'
import cv2
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import sys

import os.path
import requests

from contextlib import closing

import ssl
import time

path = "/Users/iyunshu/Desktop/aaaaaa/"


videourl = 'http://www.w3school.com.cn/i/movie.mp4'


ssl._create_default_https_context = ssl._create_unverified_context

class DownloaderSingalThread(QThread):
    singal = Signal()
    def __init__(self, path):
        QThread.__init__(self)

        self.path = path;

    def run(self):
        size = 0
        while size == 0:
            if os.path.exists(self.path):
                size = os.path.getsize(self.path)
        self.singal.emit()

class DownloaderThread(QThread):
    singal = Signal(str)
    def __init__(self, videourl, videPath):
        QThread.__init__(self)
        self.videoCapture = cv2.VideoCapture(videourl)
        self.videPath = videPath
        #指定写视频的格式, I420-avi, MJPG-mp4
        self.fps = self.videoCapture.get(cv2.CAP_PROP_FPS)

        self.fps_num = self.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
        self.size = (int(self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.videoCapture.get(cv2.cv2.CAP_PROP_FRAME_HEIGHT)))
        self.videoWriter = cv2.VideoWriter(self.videPath, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), self.fps, self.size)

    def run(self):
        success, frame = self.videoCapture.read()
        count = 0
        fileCount = 0
        while success :
            if self.videoWriter.isOpened() == False:
                self.videoWriter.open(self.videPath, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), self.fps, self.size)
            self.videoWriter.write(frame) #写视频帧
            if count > 0 and (count % (int(self.fps) * 10)) == 0:
                self.videoWriter.release()
                self.singal.emit(self.videPath)
                fileCount += 1
                self.videPath = path + str(fileCount) + '.mp4'

            count += 1
            success, frame = self.videoCapture.read() #获取下一帧
        self.videoWriter.release()
        self.videoCapture.release()



class MyThread(QThread):
    singal = Signal(float, )
    def __init__(self, path):
        QThread.__init__(self)
        print(path)
        self.videoCapture = cv2.VideoCapture(path)

        #获得码率及尺寸
        self.fps = self.videoCapture.get(cv2.CAP_PROP_FPS)
        self.fps_num = self.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)

        print(self.fps)
        print(self.fps_num)

        self.timeAmount = self.fps_num / self.fps
        self.fps_num = self.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
        m, s = divmod(self.timeAmount, 60)
        h, m = divmod(m, 60)
        self.amutnTimeFormt = "%02d:%02d:%02d" % (h, m, s)

    def run(self):
        success, frame = self.videoCapture.read()
        count = 0
        while success :

            count += 1
            cv2.imwrite('asd.jpg', frame)

            time.sleep(1/self.fps) #延迟
            pixmap = QPixmap()
            pixmap.load('asd.jpg')
            size = QSize(int(self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                         int(self.videoCapture.get(cv2.cv2.CAP_PROP_FRAME_HEIGHT)))
            self.pixmap = pixmap.scaled(size)
            self.singal.emit(count / self.fps_num)
            success, frame = self.videoCapture.read() #获取下一帧




class VideoPlayer(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        #获得视频的格式

        self.playArray = []
        self.playerThread = None

        v_box = QVBoxLayout()
        self.setContentsMargins(0,0,0,0)
        self.setLayout(v_box)

        h_box = QHBoxLayout()

        self.inputText = QLineEdit()
        h_box.addWidget(self.inputText)

        self.playBtn = QPushButton('播放')
        self.playBtn.clicked.connect(self.playBtnClick)
        h_box.addWidget(self.playBtn)

        v_box.addLayout(h_box)

        self.labe = QLabel()
        v_box.addWidget(self.labe)

        self.progressBar = QProgressBar()
        v_box.addWidget(self.progressBar)

        self.timeLab = QLabel()
        v_box.addWidget(self.timeLab)







    def playBtnClick(self):
        playUrl = videopaa
        downloadPath = path + '0.mp4'
        self.downloaderThread = DownloaderThread(playUrl, downloadPath)
        self.downloaderThread.start()
        self.downloaderThread.singal.connect(self.playAction)

    def downloadProgress(self, progress):
        print('[download]:' + str(progress))
        self.downloaderSingalThread = DownloaderSingalThread(self.downloadPath)
        self.downloaderSingalThread.start()
        self.downloaderSingalThread.singal.connect(self.playAction)

    def playAction(self, playpath):
        if self.playerThread != None and self.playerThread.isRunning():
            self.playArray.append(playpath)
        else:
            temp = ''
            if len(self.playArray) == 0:
                temp = playpath
            else:
                temp = self.playArray[0]
            self.playerThread = MyThread(temp)
            self.playerThread.start()
            self.playerThread.singal.connect(self.thresetContainer)
            self.progressBar.setFixedSize(int(self.playerThread.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)), 8)
            self.playArray.remove(temp)




    def thresetContainer(self, progress):
        currntTime = self.playerThread.timeAmount * progress
        m, s = divmod(currntTime, 60)
        h, m = divmod(m, 60)
        currntTimeFormt = "%02d:%02d:%02d" % (h, m, s)
        self.timeLab.setText(currntTimeFormt+ '/' + self.playerThread.amutnTimeFormt)

        self.labe.setPixmap(self.playerThread.pixmap)
        self.progressBar.setValue(progress * 100)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = VideoPlayer()
    ui.show()
    sys.exit(app.exec_())
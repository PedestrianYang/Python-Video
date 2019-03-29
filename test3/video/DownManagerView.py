
from PySide2.QtWidgets import *

from PySide2.QtCore import *
from video.PlayerView import *

import threading
import time
import inspect
import ctypes

class DownManagerView(QWidget):
    def __init__(self, downloaderThread):
        QWidget.__init__(self)
        self.setWindowTitle("下载管理界面")
        self.downloaderThread = downloaderThread

        self.setContainer()

    def setContainer(self):
        v_box = QVBoxLayout()
        self.listView = QListWidget()
        v_box.addWidget(self.listView)
        self.setLayout(v_box)
        for downloadThread in self.downloaderThread:
            item = DownloadItemView(downloadThread)
            item.deleteSingal.connect(self.deleteDownload)
            tempItem = QListWidgetItem()
            tempItem.setSizeHint(QSize(100, 100))
            self.listView.addItem(tempItem)
            self.listView.setItemWidget(tempItem, item)
    def deleteDownload(self, videoView):
        if videoView.videoDownloadThread != None and videoView.videoDownloadThread.downLoader.isDownloading:
            videoView.videoDownloadThread.downLoader.downloadCancel()


class DownloadItemView(QWidget):
    deleteSingal = Signal(QWidget)
    def __init__(self, videoDownloadThread):
        QWidget.__init__(self)
        self.videoDownloadThread = videoDownloadThread
        self.setContent()

    def setContent(self):
        v_box = QVBoxLayout()

        nameLab = QLabel(self.videoDownloadThread.video.name)
        v_box.addWidget(nameLab)


        h_box = QHBoxLayout()

        self.progressBar = QProgressBar()
        self.progressBar.setFixedSize(100,8)

        h_box.addWidget(self.progressBar)

        self.progressLabe = QLabel('0%')
        h_box.addWidget(self.progressLabe)

        v_box.addLayout(h_box)

        conntrol_h_box = QHBoxLayout()

        playBtn = QPushButton('播放')
        playBtn.clicked.connect(self.playBtnClick)
        conntrol_h_box.addWidget(playBtn)

        deleteBtn = QPushButton('删除')
        deleteBtn.clicked.connect(self.deleteBtnClick)
        conntrol_h_box.addWidget(deleteBtn)

        v_box.addLayout(conntrol_h_box)

        self.setLayout(v_box)

        self.videoDownloadThread.downLoader.downloadProgressSingal.connect(self.updateProgressBaraa)

    def updateProgressBaraa(self, progress):
        self.progressBar.setValue(progress)
        speed = ('%0.2f%%' % progress)
        self.progressLabe.setText(speed)

    def playBtnClick(self):
        print('播放')
        self.playerView = VideoPlayer(self.videoDownloadThread.downLoader.path)
        self.playerView.show()


    def deleteBtnClick(self):
        self.deleteSingal.emit(self)
        print('删除')



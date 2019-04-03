
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
            tempItem = QListWidgetItem()
            tempItem.setSizeHint(QSize(100, 150))
            item = DownloadItemView(downloadThread, tempItem)
            item.deleteSingal.connect(self.deleteDownload)

            self.listView.addItem(tempItem)
            self.listView.setItemWidget(tempItem, item)

    def deleteDownload(self, videoView):
        if videoView.videoDownloadThread != None and videoView.videoDownloadThread.downLoader.isDownloading:
            videoView.videoDownloadThread.downLoader.downloadCancel()
        else:
            videoView.videoDownloadThread.downLoader.deleteLater()
            videoView.videoDownloadThread.quit()
            videoView.videoDownloadThread.deleteLater()

        self.listView.takeItem(self.listView.row(videoView.tempItemView))





class DownloadItemView(QWidget):
    deleteSingal = Signal(QWidget)
    def __init__(self, videoDownloadThread, tempItemView):
        QWidget.__init__(self)
        self.videoDownloadThread = videoDownloadThread
        self.tempItemView = tempItemView
        self.setContent()

    def setContent(self):
        v_box = QVBoxLayout()

        nameLab = QLabel(self.videoDownloadThread.video.name)
        nameLab.setFixedSize(100, 20)
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

        self.stopBtn = QPushButton('暂停')
        self.stopBtn.clicked.connect(self.stopBtnClick)
        conntrol_h_box.addWidget(self.stopBtn)


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

    def stopBtnClick(self):
        if  self.videoDownloadThread.downLoader.stop:
            self.videoDownloadThread.downLoader.stop = False
            self.stopBtn.setText("暂停")
        else:
            self.stopBtn.setText("开始")
            self.videoDownloadThread.downLoader.stop = True


    def deleteBtnClick(self):
        self.deleteSingal.emit(self)
        print('删除')



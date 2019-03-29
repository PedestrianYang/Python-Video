import asyncio
import sys
import urllib

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import urllib.request


from request import Reques
from Downloader import Downloader
from DownManagerView import *
from CacheManager import CacheManager
from CacheVideoView import *

import aiohttp
import ssl
import threading
import time


ssl._create_default_https_context = ssl._create_unverified_context
path = "/Users/iyunshu/Desktop/aaaaaa/"


class MyThread(QThread):
    singal = Signal()
    def __init__(self, requestUrl, nextPage):
        QThread.__init__(self)
        self.nextPage = nextPage
        self.reqestUrl = requestUrl
        self.requet = Reques()
        self.videoModes = []

    def run(self):
        if self.nextPage == 1:
            self.videoModes = self.requet.getTargetUrl()
        elif self.nextPage > 1:
            self.videoModes = self.requet.downloadPage(self.reqestUrl)
        self.singal.emit()

class LoadImageThread(QThread):
    singal = Signal()
    def __init__(self, url):
        QThread.__init__(self)
        self.url = url


    def run(self):

        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        req = urllib.request.Request(self.url, headers=headers)
        content = urllib.request.urlopen(req).read()
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(bytearray(content)))
        self.pixmap = pixmap.scaled(60,60)

        self.singal.emit()

class VideoDownloadThread(QThread):
    singal = Signal()
    def __init__(self, video):
        QThread.__init__(self)
        self.video = video


    def run(self):
        tempPath = path + self.video.name + ".mp4"
        self.downLoader = Downloader(self.video.downUrl, tempPath)
        self.downLoader.downLoad()
        self.singal.emit()



class TitleView(QLabel):
    def __init__(self, titleMode):
        QLabel.__init__(self)
        ssl._create_default_https_context = ssl._create_unverified_context
        self.titleMode = titleMode
        self.setText(titleMode.name)

class ItemView(QWidget):

    def __init__(self, video):
        QWidget.__init__(self)
        ssl._create_default_https_context = ssl._create_unverified_context

        self.video = video
        self.container()

    def loadimage(self):

        label = QLabel()
        label.setMinimumSize(60, 60)
        label.setPixmap(self.loadImagethread.pixmap)
        self.b_layout.addWidget(label)

        nameL = QLabel()
        nameL.setText(self.video.name)
        self.b_layout.addWidget(nameL)




    def aaaaa(self):
        self.loadImagethread = LoadImageThread(self.video.imgUrl)
        self.loadImagethread.start()
        self.loadImagethread.singal.connect(self.loadimage)

    def container(self):

        self.b_layout = QVBoxLayout()

        self.setLayout(self.b_layout)
        self.aaaaa()

    def mousePressEvent(self, event):
        self.downloaderThread = VideoDownloadThread(self.video)
        self.downloaderThread.start()
        self.downloaderThread.singal.connect(self.downloadComplete)
        self.downloadThreads.append(self.downloaderThread)


    def downloadComplete(self):
        notic = self.downloaderThread.video.name + '下载完成'
        print(notic)



class MainUIaa(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        ssl._create_default_https_context = ssl._create_unverified_context

        self.threadaaa = MyThread(1, 1)
        self.threadaaa.start()
        self.threadaaa.singal.connect(self.setItemViews)
        self.downloadThreads = []

        self.setWindowTitle('视频下载')
        self.cacheManager = CacheManager()
        self.allDataArr = []
        # self.requet = Reques()

        # self.grid = QGridLayout()
        self.listView = QListWidget()
        self.container()




    def container(self):
        b_Box = QVBoxLayout()


        b_hbox = QHBoxLayout()

        downManagerbuttn = QPushButton('下载管理')
        downManagerbuttn.clicked.connect(self.showDownManagerView)
        b_hbox.addWidget(downManagerbuttn)


        cachebuttn = QPushButton('缓存数据')
        cachebuttn.clicked.connect(self.cacheDataAction)
        b_hbox.addWidget(cachebuttn)

        b_Box.addLayout(b_hbox)


        dbTablebuttn = QPushButton('查看缓存数据')
        dbTablebuttn.clicked.connect(self.showCacheView)
        b_hbox.addWidget(dbTablebuttn)

        # b_Box.addLayout(self.grid)
        b_Box.addWidget(self.listView)

        nextbuttn = QPushButton('下一页')
        nextbuttn.clicked.connect(self.requestNextPage)
        b_Box.addWidget(nextbuttn)
        self.page = 1

        self.setLayout(b_Box)


    def showDownManagerView(self):
        self.downloadManagerView = DownManagerView(self.downloadThreads)
        self.downloadManagerView.show()

    def showCacheView(self):
        self.cacheView = CacheVideoView()
        self.cacheView.show()

    def cacheDataAction(self):
        self.cacheManager.insertAll(self.allDataArr)

    def requestNextPage(self):
        print(self.page)
        netPageUrl = self.requestUrl + str(self.page) + '/'
        print(netPageUrl)

        self.nextPageThread = MyThread(netPageUrl, 2)
        self.nextPageThread.start()
        self.nextPageThread.singal.connect(self.setItemViews)


    def setItemViews(self):
        self.requestUrl = self.threadaaa.requet.newVideoUrl
        if self.page == 1:
            self.videoModes = self.threadaaa.videoModes
        elif self.page > 1:
            self.videoModes = self.nextPageThread.videoModes
        self.allDataArr.extend(self.videoModes)
        self.page += 1

        for i in range(len(self.videoModes)):
            videoMode = self.videoModes[i]
            videoView = ItemView(videoMode)

            tempItem = QListWidgetItem()
            tempItem.setSizeHint(QSize(100, 100))

            self.listView.addItem(tempItem)
            self.listView.setItemWidget(tempItem, videoView)


            # self.grid.addWidget(videoView, i / 3, i % 3)









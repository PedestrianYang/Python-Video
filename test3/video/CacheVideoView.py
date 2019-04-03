from PySide2.QtWidgets import *
from PySide2.QtCore import *
from video.CacheManager import *
from video.VideoView import *
from selenium import webdriver
from bs4 import BeautifulSoup
from video.request import *

ssl._create_default_https_context = ssl._create_unverified_context

class GetDownloadUrlThread(QThread):
    def __init__(self, video):
        QThread.__init__(self)
        self.video = video
        self.db = CacheManager()
        self.request = Reques()

    def run(self):
        resp = self.request.doRequest(self.video.videoUrl)
        soup1 = BeautifulSoup(resp, "html.parser")

        items = soup1.findAll('a')

        dowloadUrl = None
        for item in items:
            href = item.get('href')
            if href != None and href.endswith('.mp4'):
                dowloadUrl = href
                break
        self.db.updateVideoDownLoadUrl(self.video, dowloadUrl)




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

class ItemView(QWidget):
    deleteBtnClickSingal = Signal(int)
    def __init__(self, video, index):
        QWidget.__init__(self)
        self.video = video
        self.index = index
        if video.downUrl == None:
            self.getDownUrlThreead = GetDownloadUrlThread(video)
            self.getDownUrlThreead.start()
            self.getDownUrlThreead.finished.connect(self.threadDestoryAction)
        self.container()

    def threadDestoryAction(self):
        self.getDownUrlThreead.deleteLater()

    def loadimage(self):
        label = QLabel()
        label.setMinimumSize(60, 60)
        label.setPixmap(self.loadImagethread.pixmap)
        self.b_layout.addWidget(label)

        nameL = QLabel()
        nameL.setText(self.video.name)
        self.b_layout.addWidget(nameL)

        conntrol_h_box = QHBoxLayout()

        playBtn = QPushButton('在线播放')
        playBtn.clicked.connect(self.playBtnClick)
        conntrol_h_box.addWidget(playBtn)


        deleteBtn = QPushButton('删除记录')
        deleteBtn.clicked.connect(self.deleteBtnClick)
        conntrol_h_box.addWidget(deleteBtn)

        self.b_layout.addLayout(conntrol_h_box)

    def playBtnClick(self):
        self.playerView = VideoPlayer(self.video.downUrl)
        self.playerView.show()

    def deleteBtnClick(self):
        self.deleteBtnClickSingal.emit(self.index)


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



    def downloadComplete(self):
        notic = self.downloaderThread.video.name + '下载完成'
        print(notic)

class CacheVideoView(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.db = CacheManager()
        self.setContainer()
        self.loadLocalData()

    def setContainer(self):
        v_box = QVBoxLayout()

        downManagerbuttn = QPushButton('清除缓存')
        downManagerbuttn.clicked.connect(self.cleanCache)
        v_box.addWidget(downManagerbuttn)

        self.listView = QListWidget()
        v_box.addWidget(self.listView)

        self.setLayout(v_box)

    def setItemViews(self):

        for i in range(len(self.videoModes)):
            videoMode = self.videoModes[i]
            videoView = ItemView(videoMode, i)
            videoView.deleteBtnClickSingal.connect(self.deleteCacheVideo)
            tempItem = QListWidgetItem()
            tempItem.setSizeHint(QSize(100, 150))
            self.listView.addItem(tempItem)
            self.listView.setItemWidget(tempItem, videoView)

    def deleteCacheVideo(self, index):
        videoMode = self.videoModes[index]
        self.db.deleteVideo(videoMode)
        self.listView.takeItem(index)

    def cleanCache(self):
        self.db.cleanCache()

    def loadLocalData(self):
        self.videoModes = self.db.selectAllData()
        self.setItemViews()


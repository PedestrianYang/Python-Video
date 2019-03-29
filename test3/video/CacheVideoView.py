from PySide2.QtWidgets import *
from PySide2.QtCore import *
from video.CacheManager import *
from video.VideoView import *

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

    def __init__(self, video):
        QWidget.__init__(self)
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
            videoView = ItemView(videoMode)

            tempItem = QListWidgetItem()
            tempItem.setSizeHint(QSize(100, 100))

            self.listView.addItem(tempItem)
            self.listView.setItemWidget(tempItem, videoView)


    def cleanCache(self):
        self.db.cleanCache()

    def loadLocalData(self):
        self.videoModes = self.db.selectAllData()
        self.setItemViews()


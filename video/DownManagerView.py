
from PySide2.QtWidgets import *

from PySide2.QtCore import *

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
            tempItem = QListWidgetItem()
            tempItem.setSizeHint(QSize(100, 100))
            self.listView.addItem(tempItem)
            self.listView.setItemWidget(tempItem, item)

class DownloadItemView(QWidget):
    def __init__(self, videoDownloadThread):
        QWidget.__init__(self)
        self.videoDownloadThread = videoDownloadThread
        self.setContent()

    def _async_raise(self, tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def stop_thread(self, thread):
        self._async_raise(thread.ident, SystemExit)

    def setContent(self):
        v_box = QVBoxLayout()

        nameLab = QLabel(self.videoDownloadThread.video.name)
        v_box.addWidget(nameLab)


        h_box = QHBoxLayout()

        self.progressBar = QProgressBar()
        self.progressBar.setFixedSize(100,8)

        h_box.addWidget(self.progressBar)

        self.progressLabe = QLabel()
        h_box.addWidget(self.progressLabe)

        v_box.addLayout(h_box)

        self.setLayout(v_box)

        self.thread = threading.Thread(target=self.updateProgressBar, name='asdasd')
        self.thread.start()

    def updateProgressBar(self):
        progress = 0.0
        while progress < 100:
            print(progress)
            speed = ('%0.2f%%' % progress)
            self.progressLabe.setText(speed)
            progress = self.videoDownloadThread.downLoader.progress
            self.progressBar.setValue(progress)
            time.sleep(1)

    def destroy(self, *args, **kwargs):
        QWidget.destroy(self, *args, **kwargs)
        self.stop_thread(self.thread)


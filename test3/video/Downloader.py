
import os.path
import ssl
from bs4 import BeautifulSoup
from PySide2.QtCore import *
from video.request import Reques
from contextlib import closing
import time
import requests

class Downloader(QObject):
    downloadProgressSingal = Signal(float)
    def __init__(self, video_url, path):
        QObject.__init__(self)
        ssl._create_default_https_context = ssl._create_unverified_context
        self.video_url = video_url
        self.path = path
        self.request = Reques()
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless') #使用浏览器加载，却不用打开
        #
        # # driver=webdriver.Firefox(executable_path = '/usr/local/lib/python3.6/geckodriver')
        # self.driver = webdriver.Chrome(executable_path='/usr/local/lib/python3.6/chromedriver', options=chrome_options)
        # self.driver.implicitly_wait(10)
        self.progress = 0
        self.stop = False
        self.close = False
        self.isDownloading = False



    def downLoad(self):

        # self.driver.get(self.video_url) #获取浏览器内容
        # soup1 = BeautifulSoup(self.driver.page_source, "html.parser")

        resp = self.request.doRequest(self.video_url)
        soup1 = BeautifulSoup(resp, "html.parser")

        items = soup1.findAll('a')
        dowloadUrl = None
        for item in items:
            href = item.get('href')
            if href != None and href.endswith('.mp4'):
                dowloadUrl = href
                break

        print(dowloadUrl)
        self._downloader(dowloadUrl)

    def _downloader(self, dowloadUrl):
        ip = ['121.31.159.197', '175.30.238.78', '124.202.247.110', '10.0.7.555', '126.202.247.120', '128.212.117.120']
        Header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
        }

        size = 0

        if os.path.exists(self.path):
            Header['Range'] = 'bytes=%d-' % os.path.getsize(self.path)
            size = os.path.getsize(self.path)
        print('开始下载')
        with closing(requests.get(dowloadUrl, headers=Header, stream=True, verify=False)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            if content_size == size:
                print("文件已存在")
                return


            if response.status_code == 200 or response.status_code == 206:
                self.content_size = content_size/chunk_size / 1024
                self.isDownloading = True

                with open(self.path, 'wb') as f:
                    for data in response.iter_content(chunk_size=chunk_size):
                        if self.close == True:
                            self.isDownloading = False
                            break
                        if self.stop == True:
                            self.isDownloading = False
                            while self.stop:
                                time.sleep(1)

                        f.write(data)
                        size += len(data)
                        f.flush()
                        self.progress = float(size/content_size * 100)
                        self.downloadProgressSingal.emit(self.progress )
                        # self.downloadSingle.foosignal.emit(progress)


    def downloadCancel(self):
        self.close = True



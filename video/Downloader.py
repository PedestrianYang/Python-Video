
import os.path
import requests
import sys
from contextlib import closing
from selenium import webdriver
from bs4 import BeautifulSoup
from PySide2.QtCore import *
import ssl

class FooConnection(QObject):
    #Signal 创建必须在QObject类中进行
    foosignal = Signal(float)

class Downloader:

    downloadSingle = FooConnection()

    def __init__(self, video_url, path):
        ssl._create_default_https_context = ssl._create_unverified_context
        self.video_url = video_url
        self.path = path
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')

        # driver=webdriver.Firefox(executable_path = '/usr/local/lib/python3.6/geckodriver')
        self.driver = webdriver.Chrome(executable_path='/usr/local/lib/python3.6/chromedriver', options=chrome_options)
        self.driver.implicitly_wait(10)
        self.progress = 0



    def downLoad(self):
        print("111111")
        self.driver.get(self.video_url)
        print("222222")
        soup1 = BeautifulSoup(self.driver.page_source, "html.parser")
        print("333333")
        items = soup1.findAll('a')
        dowloadUrl = None
        for item in items:
            href = item.get('href')
            if href != None and href.endswith('.mp4'):
                dowloadUrl = href
                break
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

        with closing(requests.get(dowloadUrl, headers=Header, stream=True, verify=False)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            if content_size == size:
                print("文件已存在")
                return

            if response.status_code == 200:
                self.content_size = content_size/chunk_size / 1024
                sys.stdout.write('[File Size]: %0.2f MB\n' % (self.content_size))
                with open(self.path, 'wb') as f:
                    for data in response.iter_content(chunk_size=chunk_size):
                        f.write(data)
                        size += len(data)
                        f.flush()

                        self.progress = float(size/content_size * 100)
                        # self.downloadSingle.foosignal.emit(progress)

                        # sys.stdout.write('\r[Progress]: %0.2f%%' % )
                        # sys.stdout.flush()
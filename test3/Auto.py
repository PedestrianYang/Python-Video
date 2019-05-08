
import urllib.request
from selenium import webdriver
import urllib
from bs4 import BeautifulSoup
import ssl
import re
import os.path
import requests
from contextlib import closing
import sys
import time

class Request11:
    def __init__(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        self.temptargetUrl = ""
        self.path = "/Users/iyunshu/Desktop/aaaaaa/"

    def getTitle(self):

        rep = self.doRequest(self.temptargetUrl)
        soup1 = BeautifulSoup(rep,"html.parser")
        hres = soup1.findAll("a")
        a = None
        for tempa in hres:
            title = tempa.string
            if title == '最新视频':
                a = tempa
                break
        self.getVideos(a.get('href'))

    def getVideos(self, url):
        rep = self.doRequest(url)
        soup1 = BeautifulSoup(rep,"html.parser")
        hres = soup1.findAll("a")

        for href in hres:
            aaaurl = href.get('href')
            if aaaurl != None and aaaurl.find('/videos/') > 0:
                self.downLoad(aaaurl)


    def doRequest(self, requestUrl):
        print("开始请求")
        try:
            fuckyou_header= {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
            req = urllib.request.Request(requestUrl,headers=fuckyou_header)
            content = urllib.request.urlopen(req).read()
            content = content.decode('utf-8',"ignore")
        except urllib.request.URLError as e:
            if hasattr(e,"reason"):
                print (u"连接失败,错误原因",e.reason)
                return None
        return content

    def downLoad(self, videoUrl):
        print("111111")
        # self.driver.get(videoUrl)
        rep = self.doRequest(videoUrl)
        print("222222")
        soup1 = BeautifulSoup(rep, "html.parser")
        print("333333")
        items = soup1.findAll('a')

        for item in items:
            href = item.get('href')
            if href != None and href.endswith('.mp4'):
                print(href)
                time.sleep(10)


        # str1 = u"下载:"
        # str= str1 + '.*?<a href="(.*?)".*?'
        # pattern = re.compile(str,re.S)
        # items = re.findall(pattern, self.driver.page_source)
        # print(items[0])
        # tempPath = self.path + self.driver.title + ".mp4"
        # self._downloader(items[0], tempPath)

    def _downloader(self, video_url, path):
        ip = ['121.31.159.197', '175.30.238.78', '124.202.247.110', '10.0.7.555', '126.202.247.120', '128.212.117.120']
        Header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
        }

        size = 0

        if os.path.exists(path):
            Header['Range'] = 'bytes=%d-' % os.path.getsize(path)
            size = os.path.getsize(path)

        with closing(requests.get(video_url, headers=Header, stream=True, verify=False)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            if content_size == size:
                print("文件已存在")
                return

            if response.status_code == 200:
                sys.stdout.write('[File Size]: %0.2f MB\n' % (content_size/chunk_size/1024))
                with open(path, 'wb') as f:
                    for data in response.iter_content(chunk_size=chunk_size):
                        f.write(data)
                        size += len(data)
                        f.flush()
                        sys.stdout.write('\r[Progress]: %0.2f%%' % float(size/content_size*100))
                        sys.stdout.flush()

if __name__ == '__main__':
    req = Request11()
    req.getTitle()
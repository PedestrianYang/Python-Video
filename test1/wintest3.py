#coding=utf-8
import random
import time
from time import sleep


__author__ = 'ymq'
import urllib.request
from selenium import webdriver
import urllib
import sys
import re

import os.path
import requests
from bs4 import BeautifulSoup
from contextlib import closing


#coding=utf-8
import random
import time
from time import sleep


__author__ = 'ymq'
import urllib.request
from selenium import webdriver
import urllib
import sys
import re

import os.path
import requests
from bs4 import BeautifulSoup
from contextlib import closing

class DownLoadVideo:
    def __init__(self):
        self.url = "https://fcww9.com"

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')

        # driver=webdriver.Firefox(executable_path = '/usr/local/lib/python3.6/geckodriver')
        self.driver = webdriver.Chrome(executable_path=r'C:\Users\Administrator\Desktop\macAndWin\开发工具\win\chromedriver.exe', chrome_options=chrome_options)
        self.driver.implicitly_wait(10)
        self.path = r'C:\Users\Administrator\Desktop\macAndWin\开发工具\mac\other\1'


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

    def startRequest(self):
        content = self.doRequest(self.url)
        soup = BeautifulSoup(content,"html.parser")
        navigation = soup.find(attrs={"class":"navigation"})
        titles = navigation.findAll("a")

        selectBook = input("请输入视频类型：")
        title = titles[int(selectBook)]
        print(title.get("href"))
        print(title.string)
        self.downloadPage(title.get("href"), 1)


    def downloadPage(self, requestUrl, page):
        content1 = self.doRequest(requestUrl)
        soup1 = BeautifulSoup(content1,"html.parser")
        navigation1 = soup1.find(attrs={"id":"list_videos_latest_videos_list_items"})
        titles1 = navigation1.findAll('div')

        page += 1
        resArr = []


        for temp in titles1:
            temptitle = temp.a
            # print(temptitle)
            if temptitle != None:
                temptitleHref = temptitle.get("href")
                print(temptitleHref)
                if temptitleHref != "#":
                    resArr.append(temptitleHref)
        print(resArr)

        count = 0

        while( count < len(resArr)):
            aaaa = resArr[count]
            print("开始下载" + aaaa)
            self.driver.get(aaaa)

            str1 = u"下载:"
            str= str1 + '.*?<a href="(.*?)".*?'
            pattern = re.compile(str,re.S)
            items = re.findall(pattern, self.driver.page_source)
            print(items[0])

            tempPath = self.path + self.driver.title + ".mp4"

            self._downloader(items[0], tempPath)
            time.sleep(10)

            count += 1

        t = time.time()
        nowdate = lambda:int(round(t * 1000))
        netPageUrl = requestUrl + '?mode=async&function=get_block&block_id=list_videos_latest_videos_list&sort_by=post_date&from=%s&_=%s' % (page, nowdate)
        print("下载完毕")
        self.downloadPage(netPageUrl, page)


aaa = DownLoadVideo()
aaa.startRequest()


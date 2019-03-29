from VideoModel import Video, Title

__author__ = 'ymq'
import urllib.request
from selenium import webdriver
import urllib
import sys
import re
import time

import os.path
import requests
from bs4 import BeautifulSoup
from contextlib import closing
import ssl
from Downloader import Downloader

class Reques:
    def __init__(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        self.oriUrl = "https://github.com/fcwporn/-/wiki"
        self.temptargetUrl = "https://fcww11.com"


    def getTargetUrl(self):
        # rep = self.doRequest(self.oriUrl)
        # soup1 = BeautifulSoup(rep,"html.parser")
        # div = soup1.find(attrs={'class':'markdown-body'})
        # hres = div.findAll('a')
        # urls = []
        # for a in hres:
        #     if a.string.startswith('https://fcw') or a.string.startswith('http://fcw'):
        #         urls.append(a.string)

        rep = self.doRequest(self.temptargetUrl)
        soup1 = BeautifulSoup(rep,"html.parser")
        hres = soup1.findAll("a")
        a = None
        for tempa in hres:
            title = tempa.string
            if title == '最新视频':
                a = tempa
                break

        return self.downloadPage(a.get('href'))



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

    def downloadPage(self, requestUrl):
        self.newVideoUrl = requestUrl
        content1 = self.doRequest(requestUrl)
        soup1 = BeautifulSoup(content1,"html.parser")

        navigation1 = soup1.find(attrs={"id":"list_videos_latest_videos_list_items"})
        titles1 = navigation1.findAll('div')
        resArr = []

        for temp in titles1:
            temptitle = temp.a
            # print(temptitle)
            if temptitle != None:
                temptitleHref = temptitle.get("href")

                # print(temptitleHref)
                if temptitleHref != "#":
                    temptitleHrefTitle = temptitle.get("title")
                    imgUrl = temp.img.get("data-original")
                    videoMode = Video(temptitleHrefTitle, imgUrl, temptitleHref)
                    resArr.append(videoMode)
        return resArr


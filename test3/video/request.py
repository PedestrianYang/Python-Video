from video.VideoModel import Video, Title

__author__ = 'ymq'
import urllib.request
import urllib
from bs4 import BeautifulSoup
import ssl

class Reques:
    def __init__(self):
        ssl._create_default_https_context = ssl._create_unverified_context

        self.temptargetUrl = ""


    def getTargetUrl(self):


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


# coding:utf-8
#只查询硬座与二等座
import urllib.request
import urllib
import json
import ssl
import stationOBJ

ssl._create_default_https_context = ssl._create_unverified_context



class qiangPiao():
    def __init__(self):
        self.train_date = ""
        self.from_station = ""
        self.to_station = ""

    def getTicketList(self):
        resule = self.getRequest()
        ticketInfos = []
        for i in resule:
            tempArr = i.split('|')

            yingzhuo = '0'
            if tempArr[29]:
                yingzhuo = tempArr[29]

            erdeng = '0'
            if tempArr[30]:
                erdeng = tempArr[30]

            ticketInfo = {"车次":tempArr[3], "硬座：":yingzhuo, "二等座：": erdeng}
            ticketInfos.append(ticketInfo)

        return ticketInfos





    def getRequest(self):
        url = 'https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT' % (self.train_date, self.from_station, self.to_station)
        print(url)
        req = urllib.request.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
        html = urllib.request.urlopen(req).read().decode('utf-8', 'ignore')
        dict = json.loads(html)
        result = dict['data']['result']
        return result

    def start(self):
        self.train_date = input("请输入出发时间（格式：2018-09-29）：")
        station = {}
        for i in stationOBJ.stations.split('@'):
            if i:
                tmp = i.split('|')
                station[tmp[1]] = tmp[2]

        self.from_station = station[input('请输入出发城市：')]
        self.to_station = station[input('请输入到达城市：')]

        print(self.getTicketList())

qiangPiao = qiangPiao()
qiangPiao.start()
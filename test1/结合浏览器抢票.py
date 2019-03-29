from time import sleep

from selenium import webdriver
from bs4 import BeautifulSoup
import stationOBJ
from splinter.browser import Browser
import re

"""网址"""
ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
login_url = "https://kyfw.12306.cn/otn/login/init"
initmy_url = "https://kyfw.12306.cn/otn/view/index.html"
buy="https://kyfw.12306.cn/otn/confirmPassenger/initDc"

cities= {'成都':'%u6210%u90FD%2CCDW',
         '重庆':'%u91CD%u5E86%2CCQW',
         '北京':'%u5317%u4EAC%2CBJP',
         '广州':'%u5E7F%u5DDE%2CGZQ',
         '杭州':'%u676D%u5DDE%2CHZH',
         '宜昌':'%u5B9C%u660C%2CYCN',
         '郑州':'%u90D1%u5DDE%2CZZF',
         '深圳':'%u6DF1%u5733%2CSZQ',
         '西安':'%u897F%u5B89%2CXAY',
         '大连':'%u5927%u8FDE%2CDLT',
         '武汉':'%u6B66%u6C49%2CWHN',
         '上海':'%u4E0A%u6D77%2CSHH',
         '南京':'%u5357%u4EAC%2CNJH',
         '合肥':'%u5408%u80A5%2CHFH'}

class halfAutoGetTicket():
    def __init__(self):
        self.driver_name='chrome'
        self.executable_path='/usr/local/lib/python3.6/chromedriver'
        # # self.driver = webdriver.Chrome(executable_path='/usr/local/lib/python3.6/chromedriver')
        # self.driver.implicitly_wait(10)
        self.driver=Browser(driver_name=self.driver_name,executable_path=self.executable_path)
        self.driver.driver.set_window_size(1400, 1000)
        self.username = '314510591@qq.com'
        self.passwd = 'yangmeng123'
        self.train_date = '2018-12-29'
        self.from_station = '%u90D1%u5DDE%2CZZF'
        self.to_station = '%u5317%u4EAC%2CBJP'

        self.order = 0
        self.users = ''

    def login(self):


        self.driver.visit(login_url)
        # 填充密码
        self.driver.fill("loginUserDTO.user_name", self.username)
        # sleep(1)
        self.driver.fill("userDTO.password", self.passwd)
        print(u"等待验证码，自行输入...")
        while True:
            if self.driver.url != initmy_url:
                print('--------')
                sleep(1)
            else:
                print('+++++++++')
                break

    def getTickets(self):

        # self.driver=Browser(driver_name=self.driver_name,executable_path=self.executable_path)
        # self.driver.driver.set_window_size(1400, 1000)
        # self.driver.visit("file:///Users/iyunshu/Desktop/1111.htm")

        # soup = BeautifulSoup(tempHtml, 'html.parser')
        html = self.driver.html#获取网页的html数据
        soup = BeautifulSoup(html,'html.parser')
        table = soup.find(id="queryLeftTable")

        while len(table.findAll('tr')) == 0:
            html = self.driver.html#获取网页的html数据
            soup = BeautifulSoup(html,'html.parser')
            # soup = BeautifulSoup(tempHtml, 'html.parser')
            table = soup.find(id="queryLeftTable")

        name=[]

        tickets = []



        tableTitle = soup.find(id = 't-list')

        aaa = tableTitle.table.tbody



        coutn = 0


        for tr in aaa.findAll('tr'):
            ticketinfo = {}
            id = tr.get('id')
            train_id = id.split('_')[1]

            if len(tr.findAll('td')) == 13:
                id = 'train_num_%d' % coutn
                coutn += 1
                nameTd = tr.findAll('td')[0]

                div1 = nameTd.find(id = id)
                tempsoup =  BeautifulSoup(str(div1), 'html.parser')
                div2 = tempsoup.find_all('div', class_='train')
                name = div2[0].div.a.get_text()

                ticketinfo["车次"] = name
                erdengTD  = tr.findAll('td')[3]

                yingzuoTD  = tr.findAll('td')[9]


                erdeng = 'ZE_'+ train_id
                if erdengTD.get('id') == erdeng:
                    if yingzuoTD.div:
                        ticketinfo["二等"] = erdengTD.div.get_text()
                    else:
                        ticketinfo["二等"] = erdengTD.get_text()

                yingzuo = 'YZ_'+ train_id
                if yingzuoTD.get('id') == yingzuo:
                    if yingzuoTD.div:
                        ticketinfo["硬座"] = yingzuoTD.div.get_text()
                    else:
                        ticketinfo["硬座"] = yingzuoTD.get_text()

                yuedingTD = tr.findAll('td')[12].a
                print(yuedingTD)
                if ticketinfo["二等"] != '--' or ticketinfo["硬座"] != '--' :
                    if ticketinfo["二等"] != '无' or ticketinfo["硬座"] != '无' :
                        self.driver.evaluate_script(yuedingTD.onclick)


            tickets.append(ticketinfo)




        print(tickets)

    def start(self):
        self.login()
        self.driver.visit(ticket_url)
        try:
            print("购票页面开始...")
            # sleep(1)
            # 加载查询信息


            self.driver.cookies.add({"_jc_save_fromStation": self.from_station})
            self.driver.cookies.add({"_jc_save_toStation": self.to_station})
            self.driver.cookies.add({"_jc_save_fromDate": self.train_date})

            self.driver.reload()

            count=0
            if self.order!=0:
                while self.driver.url == ticket_url:
                    self.driver.find_by_text(u"查询").click()
                    count += 1
                    print("循环点击查询... 第 %s 次" % count)

                    # sleep(1)
                    # try:
                    #     self.driver.find_by_text(u"预订")[self.order - 1].click()
                    # except Exception as e:
                    #     print (e)
                    #     print ("还没开始预订")
                    #     continue
            else:
                while self.driver.url == ticket_url:
                    self.driver.find_by_text(u"查询").click()
                    count += 1
                    print ("循环点击查询... 第 %s 次" % count)
                    self.getTickets()
                    # sleep(0.8)
                    # try:
                    #     for i in self.driver.find_by_text(u"预订"):
                    #         i.click()
                    #         sleep(1)
                    # except Exception as e:
                    #     print (e)
                    #     print ("还没开始预订 %s" %count)
                    #     continue
            print ("开始预订...")
            # sleep(3)
            # self.driver.reload()
            sleep(1)
            print ('开始选择用户...')
            for user in self.users:
                self.driver.find_by_text(user).last.click()

            print ("提交订单...")
            sleep(1)
            # self.driver.find_by_text(self.pz).click()
            # self.driver.find_by_id('').select(self.pz)
            # # sleep(1)
            # self.driver.find_by_text(self.xb).click()
            # sleep(1)
            self.driver.find_by_id('submitOrder_id').click()
            # print u"开始选座..."
            # self.driver.find_by_id('1D').last.click()
            # self.driver.find_by_id('1F').last.click()

            sleep(1.5)
            print ("确认选座...")
            self.driver.find_by_id('qr_submit_id').click()

        except Exception as e:
            print (e)
halfAutoGetTicket = halfAutoGetTicket()
halfAutoGetTicket.start()
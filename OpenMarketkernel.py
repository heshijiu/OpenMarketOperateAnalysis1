#!/usr/bin/Python
# -*- coding: utf-8 -*-

import re
import pandas as pd
import datetime
from collections import Iterator, Iterable
import requests
import jsbeautifier
import js2py
from bs4 import BeautifulSoup as Bf

def GetNowDate():
    nowTime = datetime.datetime.now()
    date = nowTime.strftime("%Y-%m-%d")
    return date
def GetNextNDate(date, days = 0):
    nextDate = date + datetime.timedelta(days)
    return nextDate
class OpenMarketOperation:
    __date = None
    __anoumt = 0
    __time_limit = 0
    __interstRate = 0
    def __init__(self, date = None, amount = 0, time = 0, interestRate = 0):
        if(date == None):
            return
        self.__date = date
        self.__anoumt = amount
        self.__time_limit = time
        self.__interstRate = interestRate
    def GetDate(self):
        return self.__date
    def GetAmount(self):
        return self.__anoumt
    def GetTimeLimit(self):
        return self.__time_limit
    def GetinterestRate(self):
        return self.__interstRate
    def IsTimeUp(self):
        startDate = datetime.datetime.strptime(self.__date, "%Y-%m-%d")
        endDate = GetNextNDate(startDate, self.__time_limit)
        nowDate = datetime.datetime.now()
        if nowDate > endDate:
            return True
        else:
            return False
    def IsTimeUpinTheDay(self, date):
        startDate = datetime.datetime.strptime(self.__date, "%Y-%m-%d")
        endDate = GetNextNDate(startDate, self.__time_limit)
        targetDate = datetime.datetime.strptime(date, "%Y-%m-%d")
        if targetDate >= endDate or targetDate < startDate:
            return True
        else:
            return False
#OMO openmarketoperation
class OMOIteraor(Iterator):
    def __init__(self, arrs):
        self.index = 0
        self.arrs = arrs
    def __next__(self):
        if self.index > len(self.arrs) - 1:
            raise StopIteration
        else:
            self.index += 1
            return self.arrs[self.index - 1]

class OMOArray(Iterable):
    __OMOList = []
    __size = 0
    def __init__(self, List = []):
        self.__OMOList = List
        self.__size = len(List)
        return
    def GetSize(self):
        return self.__size
    def Append(self, item = None):
        if item == None:
            return
        self.__OMOList.append(item)
        self.__size = len(self.__OMOList)
        return
    def AppendList(self, items = None):
        if items == None:
            return
        for item in items:
            self.__OMOList.append(item)
        self.__size = len(self.__OMOList)
        return
    def GetAmountIntime(self):
        TotalAmount = 0
        for item in self.__OMOList:
            if item.IsTimeUp() != True:
                TotalAmount += item.GetAmount()
        return TotalAmount
    def GetAmountIntimeTillTheDay(self,date):
        TotalAmount = 0
        for item in self.__OMOList:
            if item.IsTimeUpinTheDay(date) != True:
                TotalAmount += item.GetAmount()
        return TotalAmount
    def ReadCSV(self,filename = None):
        if filename == None:
            return
        df = pd.read_csv(filename, encoding='utf-8')
        count = len(df)
        i = 0
        while i < count:
            date = df['date'][i]
            amount = float(df['amount'][i])
            timeLimit = int(df['timeLimit'][i])
            interestRate = float(df['interestRate'][i])
            OMO = OpenMarketOperation(date, amount, timeLimit, interestRate)
            self.Append(OMO)
            i += 1
    def ToCSV(self,filename = None):
        if filename == None:
            return
        dateList = []
        amountList = []
        timeLimitList = []
        interestRatList = []
        for item in self.__OMOList:
            dateList.append(item.GetDate())
            amountList.append(item.GetAmount())
            timeLimitList.append(item.GetTimeLimit())
            interestRatList.append(item.GetinterestRate())
        df = pd.DataFrame({'date': dateList, 'amount': amountList, 'timeLimit': timeLimitList, 'interestRate': interestRatList})
        df.to_csv(filename, index = False, encoding='utf-8')
        print("Print csv file done!")
        return
    def __iter__(self):
        return OMOIteraor(self.__OMOList)
    def Clear(self):
        self.__OMOList = []


def GetTableUrl(i):
    front = "http://www.pbc.gov.cn/zhengcehuobisi/125207/125213/125431/125475/17081/index"
    back = ".html"
    return front+str(i)+back

def GetDate(driver):
    try:
        date = driver.find_element_by_id("shijian").text
        if len(date) == 19:
            date = date.split(" ")
            date = date[0]
        return date
    except:
        return None
def HandleContent(driver, date = None):
    isZoomExit = False
    target = []
    try:
        content = driver.find_element_by_id("zoom")
        isZoomExit = True
    except:
        print("Read zoom failed!")
        isZoomExit = False
    if isZoomExit:
        isTableExit = False
        try:
            table = content.find_elements_by_xpath("table/tbody/tr")
            isTableExit = True
        except:
            print("No table")
            isTableExit = False
        if isTableExit:
            i = 1
            for item in table:
                if i > 1:
                    target.append(CreatOpenMarketOperation(item.text,date))
                i += 1
    return target
def CreatOpenMarketOperation(item = None, date = None):
    if item == None:
        return None
    item = re.sub(" ", "", item)
    content = item.split("\n")
    timeLimit = 0
    amount = 0
    intersetRate = 0
    for thing in content:
        n = len(thing)
        if n == 0:
            continue
        if thing[n-1] == '天':
            timeLimit = int(re.sub("\D", "", thing))
            continue
        if thing[n-1] == '年':
            timeLimit = 365 * int(re.sub("\D", "", thing))
            continue
        if thing[n-1] == '月':
            timeLimit = 30 * int(re.sub("\D", "", thing))
            continue
        if thing[n-1] == '元':
            amount = float(re.sub("\D", "", thing))
            continue
        if thing[n-1] == '%':
            intersetRate = float(re.sub("\D", "", thing))
            continue
    return OpenMarketOperation(date, amount, timeLimit, intersetRate)

def GetPBCPageSourceCode(url = None):
    if url ==None:
        return None
    try:
        host_url = 'http://www.pbc.gov.cn/'
        dest_url = url
        r = requests.session()
        content = r.get(dest_url).content
        re_script = re.search(r'<script type="text/javascript">(?P<script>.*)</script>', content.decode('utf-8'),
                              flags=re.DOTALL)
        script = re_script.group('script')
        script = script.replace('\r\n', '')
        res = jsbeautifier.beautify(script)
        jscode_list = res.split('function')
        var_ = jscode_list[0]
        var_list = var_.split('\n')
        template_js = var_list[3]
        template_py = js2py.eval_js(template_js)
        function1_js = 'function' + jscode_list[1]
        position = function1_js.index('{') + 1
        function1_js = function1_js[:position] + var_ + function1_js[position:]
        function1_py = js2py.eval_js(function1_js)
        cookie1 = function1_py(str(template_py))
        cookies = {}
        cookies['wzwstemplate'] = cookie1
        function3_js = 'function' + jscode_list[3]
        position = function3_js.index('{') + 1
        function3_js = function3_js[:position] + var_ + function3_js[position:]
        function3_py = js2py.eval_js(function3_js)
        middle_var = function3_py()
        cookie2 = function1_py(middle_var)
        cookies['wzwschallenge'] = cookie2
        dynamicurl = js2py.eval_js(var_list[0])
        r.cookies.update(cookies)
        content = r.get(host_url + dynamicurl).content
        return content.decode('utf-8')
    except:
        print("Get source page failed!")
        print("and url is " + url)
        return None

def HandPBCcontent(url = None):
    if url == None:
        return None
    try:
        target = []
        soup = Bf(GetPBCPageSourceCode(url), 'html.parser')
        date = soup.find("span", {"id":"shijian"}).get_text()
        date = date.split(" ")
        date = date[0]
        content = soup.find("table", {"align": "center", "border": "1"})
        trs = content.tbody.find_all("tr")
        for i in range(1, len(trs)):
            item = trs[i].get_text()
            target.append(CreatOpenMarketOperation(item, date))
        return target
    except:
        print("Failed to Get content!")
        print("and url is " + url)
        return None
def GetTitleContent(pageIndex = 1):
    url = GetTableUrl(1)
    soup = Bf(GetPBCPageSourceCode(url), 'html.parser')
    content = soup.find_all('td', {"align": "left", "height": "22"})
    hostUrl = "http://www.pbc.gov.cn"
    contents = []
    for title in content:
        item = {}
        item["url"] = hostUrl + title.a["href"]
        item["title"] = title.a["title"]
        contents.append(item)
    return(contents)

if __name__ == "__main__":
    '''
    url = GetTableUrl(1)
    soup = Bf(GetPBCPageSourceCode(url),'html.parser')
    content =  soup.find_all('td', {"align":"left", "height" :"22"})
    for i in content:
        print(i.a["href"])
        print(i.a["title"])
        print(i.span.get_text())
    '''
    url = "http://www.pbc.gov.cn/zhengcehuobisi/125207/125213/125431/125475/3419535/index.html"
    target = HandPBCcontent(url)
    print(target)

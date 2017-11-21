#!/usr/bin/Python
# -*- coding: utf-8 -*-
from OpenMarketkernel import OMOArray, HandPBCcontent, GetTitleContent
import re
import pandas as pd
import datetime

def UpdateInit():
    fo = open("update_init.dat", 'r')
    date = fo.read()
    fo.close()
    return date

def UpdateInitFile(date):
    fo = open("update_init.dat", 'r+')
    fo.write(date)
    fo.close()

def UpdateUrlTable():
    initdate = UpdateInit()
    initdate = initdate.split('-')
    i = 1
    count = 20
    df = pd.DataFrame({'title': [], 'url': []})
    maxyear = int(initdate[0])
    maxnum = int(initdate[1])
    while i < count:
        breakFlag = False
        detial = GetTitleContent(i)
        for things in detial:
            itemUrl = things["url"]
            title = things["title"]
            titlestr = title.split('第')
            year = int(re.sub("\D", "", titlestr[0]))
            num = int(re.sub("\D", "", titlestr[1]))
            if year > maxyear:
                maxyear = year
            if num > maxnum:
                maxnum = num
            if year >= int(initdate[0]) and num > int(initdate[1]):
                df = df.append({'title': title, 'url': itemUrl}, ignore_index=True)
                print(title)
            else:
                breakFlag = True
                break
        if breakFlag:
            break
        i += 1
    resault = OMOArray()
    for url in df['url']:
        target = HandPBCcontent(url)
        resault.AppendList(target)
        print(resault.GetSize())
    resault.ReadCSV('2016-2017OMO.csv')
    resault.ToCSV('2016-2017OMO.csv')
    UpdateInitFile(str(maxyear) + '-' + str(maxnum))

if __name__ == '__main__':
    UpdateUrlTable()

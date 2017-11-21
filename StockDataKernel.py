#!/usr/bin/Python
# -*- coding: utf-8 -*-
import tushare as ts
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def ReverseList(alist = None):
    if alist == None:
        return None
    count = len(alist)
    i = 0
    reverseList = []
    while i < count:
        reverseList.append(alist[count - 1 - i])
        i += 1
    return reverseList


def GetStockPlotData(stockCode = None, item = 'close', start=None, end = None): # item = 'open','high','close','low'
    if stockCode == None or start == None or end == None:
        return None
    df = ts.get_hist_data(stockCode, start = start, end = end)
    data = {}
    data['date'] = list(df.index)
    if isinstance(item, list):
        for i in item:
            data[i] = list(df[i])
    else:
        data[item] = list(df[item])
    return data

def GetShiborData(item = None,year = 2017):# item = 'ON', '1W','2W','1M','6M','9M', '1Y'
    if item == None:
        return None
    df = ts.shibor_data(year)
    data = {}
    data['date'] = df['date']
    if isinstance(item, list):
        for i in item:
            data[i] = df[i]
    else:
        data[item] = df[item]
    return data


if __name__ == "__main__":
    df = ts.shibor_data(2017)
    print(list(df.index))

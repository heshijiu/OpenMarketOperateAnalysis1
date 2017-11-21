#!/usr/bin/Python
# -*- coding: utf-8 -*-

from OpenMarketkernel import OMOArray, GetNextNDate
from StockDataKernel import GetStockPlotData, GetShiborData
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def PlotResult(start = '2017-01-03', end = '2017-01-04'):
    omoarray = OMOArray()
    omoarray.Clear()
    omoarray.ReadCSV('2016-2017OMO.csv')
    date = datetime.datetime.strptime(start, "%Y-%m-%d")
    i = 0
    endDate = datetime.datetime.strptime(end, "%Y-%m-%d")
    resault = []
    dateList = []
    while date <= endDate:
        strDate = date.strftime("%Y-%m-%d")
        dateList.append(strDate)
        amount = omoarray.GetAmountIntimeTillTheDay(strDate)
        resault.append(amount)
        print(strDate + ":"+str(amount))
        date = GetNextNDate(date, 1)
    x = range(0, len(resault), 20)
    x = list(x)
    xdate = [dateList[index] for index in x]
    stockData = GetStockPlotData('sh', 'close', start, end)

    x1 = [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in dateList]
    x2 = [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in stockData['date']]
    plt.figure()
    plt.subplot(211)
    plt.plot(x1, resault)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.subplot(212)
    plt.plot(x2, stockData['close'])
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.show()
    del omoarray

if __name__ == '__main__':
    start = '2015-11-05'
    end = '2015-11-05'
    omoarray = OMOArray()
    omoarray.ReadCSV('test.csv')
    amount = omoarray.GetAmountIntimeTillTheDay(start)
    print(amount)





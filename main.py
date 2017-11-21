#!/usr/bin/Python
# -*- coding: utf-8 -*-

from UpdateUrlTable import UpdateUrlTable
from DBtest import PlotResult

if __name__ == "__main__":
    quit = False
    while quit == False:
        print('1.Update: Press u')
        print('2.Plot  : Press p')
        print('3.Quit  : Press q')
        command = input("Please input your command:")
        if command == 'u':
            UpdateUrlTable()
        elif command == 'p':
            start = input('input start date 2017-01-03 for example:')
            end = input('input end date 2017-01-03 for example  :')
            PlotResult(start, end)
        elif command == 'q':
            quit = True
        else:
            print('Wrong command, please inout again')










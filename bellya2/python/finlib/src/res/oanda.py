import time
from time import mktime

from datetime import datetime
from datetime import timedelta

import sys
from collections import deque

import matplotlib.pyplot as plt


class Bar:
    def __init__(self, period, handler):
        self.period = period
        self.handler = handler
        
        self.bar_end = datetime.fromtimestamp(0)
        self.last_ask = 0

    def handleTick(self, tick):

        if tick[0] >= self.bar_end:
            if self.last_ask > 0:
                bar = (self.bar_start, self.last_ask)
                self.handler.handleBar(bar)

            ts = tick[0]
            secs = ((ts.hour * 60 + ts.minute) * 60) + ts.second
            this_bar = secs / self.period
            this_bar = this_bar * self.period
            this_bar, bar_secs = divmod(this_bar, 60)    
            bar_hrs, bar_mins = divmod(this_bar, 60) 
               
            self.bar_start = datetime(ts.year, ts.month, ts.day, bar_hrs, bar_mins, bar_secs)
            
            self.bar_end = self.bar_start + timedelta(seconds=self.period)

        self.last_ask = tick[2]


class RSMA:
    def __init__(self, period):
        self.period = period
        self.win = deque()
        self.running_sum = 0
        self.value = 0

    def add(self, value):
        self.win.append(value)
        self.running_sum = self.running_sum + value        
        if len(self.win) > self.period:
            self.running_sum = self.running_sum - self.win.popleft()
        self.value = self.running_sum / len(self.win)


class Test:
    def __init__(self):
        self.bar = Bar(60, self)
        self.sma1 = RSMA(10)
        self.sma2 = RSMA(20)
        self.sma3 = RSMA(40)
        self.pos = 0
        self.buy = False
        self.sell = False
        self.pnl = 0
        
        self.dates = []
        self.asks = []
        self.sma1list = []
        self.sma2list = []
        self.sma3list = []

    def handleTick(self, tick):
        if self.buy:
            print 'buying at: ' + str(tick[2])
            self.pnl = self.pnl - tick[2]
            self.pos = 1
            self.buy = False

        if self.sell:
            self.pnl = self.pnl + tick[1]
            print 'selling at: ' + str(tick[1])
            print 'pnl: ' + str(self.pnl)
            self.pos = 0
            self.sell = False
        
        
        self.spread = tick[2] - tick[1]
        self.bar.handleTick(tick)

    def handleBar(self, bar):        
        self.sma1.add(bar[1])
        self.sma2.add(bar[1])
        self.sma3.add(bar[1])

        self.dates.append(bar[0])
        self.asks.append(bar[1] / 100000000.0)
        self.sma1list.append(self.sma1.value / 100000000.0)
        self.sma2list.append(self.sma2.value / 100000000.0)
        self.sma3list.append(self.sma3.value / 100000000.0)
        

        if self.pos == 0:
            if self.sma1.value > self.sma2.value and self.spread <= 9000:
                self.buy = True
        else:
            if self.sma1.value < self.sma3.value or self.spread > 11000:
                self.sell = True
                
                
    def handleEOD(self):
        self.plot()
                

    def plot(self):
    
        plt.plot(self.dates, self.asks)
        plt.plot(self.dates, self.sma1list)
        plt.plot(self.dates, self.sma2list)
        plt.plot(self.dates, self.sma3list)

        plt.show()
        

def parseDatetime(v):
    return  datetime.fromtimestamp(mktime(time.strptime(v, "%d/%m/%y %H:%M:%S")))

def parsePrice(v):
    d = v.index('.')
    return int(v[:d]) * 100000000 + int(v[d + 1:]) * 1000

def parseTick(line):
    timestamp = parseDatetime(line[:17])
    bid = parsePrice(line[18:25])
    ask = parsePrice(line[26:33])
    return (timestamp, bid, ask)    

def main():
    mdfilename = 'C:\\ahmad\\data\\20100317.txt'
    mdfile = open(mdfilename, 'r')

    test = Test()
    
    count = 0
    while True:
        line = mdfile.readline()
        count = count + 1
        if line :
            tick = parseTick(line)
            test.handleTick(tick)
            
#            if count == 200:
#                break
        else:
            break
    test.handleEOD()

if __name__ == '__main__':
    main()


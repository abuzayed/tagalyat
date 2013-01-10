import time
import sys
from collections import deque

class Bar:
    def __init__(self, period, handler):
        self.period = period
        self.handler = handler
        self.current_bar = 0
        self.last_ask = 0

    def handleTick(self, tick):
        ts = tick[0]
        secs = ((ts.tm_hour * 60 + ts.tm_min) * 60) + ts.tm_sec
        this_bar = secs / self.period

        if this_bar != self.current_bar:
            self.current_bar = this_bar
            if self.last_ask > 0:
                bar = (self.last_ask)
                self.handler.handleBar(bar)
        
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
        self.sma1.add(bar)
        self.sma2.add(bar)
        self.sma3.add(bar)
#        print 'Test.handleBar: bar=' + str(bar) + ', sma1=' + str(self.sma1.value) + ', sma2=' + str(self.sma2.value) + ', sma3=' + str(self.sma3.value)

        if self.pos == 0:
            if self.sma1.value > self.sma2.value and self.spread <= 9000:
                self.buy = True
        else:
            if self.sma1.value < self.sma3.value or self.spread > 11000:
                self.sell = True
            

def parseDatetime(v):
    return time.strptime(v, "%d/%m/%y %H:%M:%S")

def parsePrice(v):
    d = v.index('.')
    return int(v[:d]) * 100000000 + int(v[d + 1:]) * 1000

def parseTick(line):
    timestamp = parseDatetime(line[:17])
    bid = parsePrice(line[18:25])
    ask = parsePrice(line[26:33])
    return (timestamp, bid, ask)    

def main():
    mdfilename = 'C:\\ahmad\\data\\EC0299F7A8DE9926DAF7F2A6B2093F43.txt'
    mdfile = open(mdfilename, 'r')

    test = Test()
    
    count = 0
    while True:
        line = mdfile.readline()
        count = count + 1
        if line :
            tick = parseTick(line)
            test.handleTick(tick)
            
#            if count == 100:
#                break
        else:
            break

if __name__ == '__main__':
    main()


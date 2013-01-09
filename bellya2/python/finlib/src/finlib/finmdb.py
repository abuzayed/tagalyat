import pymongo
from pymongo import MongoClient

from datetime import date                                                                    
from datetime import timedelta                                                                      

class FinMongoDB(object):
    def __init__(self, server, port, database, yahoo):
        self.server = server
        self.port = port
        self.database = database
        self.yahoo = yahoo
    
    
    def connect(self):
        connection = MongoClient(self.server, self.port)
        self.db = connection[self.database]
        
#        self.db.drop_collection("securities")
#        self.db.drop_collection("md")
#        self.db.drop_collection("lastmd")
        
        self.db.securities.ensure_index("symbol")
        self.db.md.ensure_index([("symbol", pymongo.ASCENDING), ("date", pymongo.ASCENDING)])
        self.db.lastmd.ensure_index("symbol")


    def createSecurity(self, symbol, desc):
        security = {"symbol": symbol, "desc": desc}
        self.db.securities.insert(security)
        
        
    def getSecBySym(self, symbol):
        return self.db.securities.find_one({"symbol": symbol})


    def getOrCreateSec(self, symbol):
        sec = self.getSecBySym(symbol)
        if sec == None:
            self.createSecurity(symbol, '')
            sec = self.getSecBySym(symbol)
        return sec
        
        
    def insertHistory(self, symbol, history):
        
        dates = history['dates']
        opens = history['opens']
        highs = history['highs']
        lows = history['lows']
        closes = history['closes']
        volumes = history['volumes']
        adj_closes = history['adj_closes']
        
        N = len(dates)
        for i in range(N):
            h = {"symbol": symbol,
                "date" : dates[i],
                "open" : opens[i],
                "high" : highs[i],
                "low" : lows[i],
                "close" : closes[i],
                "adj_close" : adj_closes[i],
                "volume" : volumes[i]}
            self.db.md.insert(h)

        self.db.lastmd.update({"symbol": symbol}, {"$set": {"lastmd": dates[N - 1]}}, upsert=True)

        
    def getLastHistoryDate(self, security):
        lastmd = self.db.lastmd.find_one({"symbol": security['symbol']})
        if lastmd == None:
            return None
        else:
            return lastmd['lastmd'].date()
    

    def getHistoryFrom(self, security, start):
        return self.db.md.find({"symbol": security['symbol'], "date": {"$gte": start}})


    def updateHistory(self, security):
        today = date.today()                                                                        
        last = self.getLastHistoryDate(security)
        
        if last == None:
            history = self.yahoo.fetch(security)
            if history != None:
                self.insertHistory(security['symbol'], history)
        elif today > last:
            from_date = last + timedelta(days=1)
            history = self.yahoo.fetch(security, from_date, today)
            if history != None:
                self.insertHistory(security['symbol'], history)


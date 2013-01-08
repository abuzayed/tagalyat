import MySQLdb
from finlib import Security
from finlib import History
from datetime import date                                                                    
from datetime import timedelta                                                                      
from yahoo import Yahoo                                                                      

class FinDB(object):
    def __init__(self, server, database, user, password):
        self.server = server
        self.database = database
        self.user = user
        self.password = password
    
    def connect(self):
        self.conn = MySQLdb.connect(self.server, self.user, self.password, self.database)
        self.cur = self.conn.cursor()

    def createSecurity(self, symbol, desc):
        if self.getSecBySym(symbol) != None:
            return False
        sql = "INSERT INTO SECURITY (SYMBOL,DESCRIPTION) VALUES('" + symbol + "','" + desc + "')"
        if self.cur.execute(sql) == 1 :
            return True
        else:
            return False
        
    def getSecBySym(self, symbol):
        sql = "SELECT ID, SYMBOL, DESCRIPTION FROM SECURITY WHERE SYMBOL='" + symbol + "'"
        count = self.cur.execute(sql)
        if count == 0:
            return None
        res = self.cur.fetchall()
        return Security(res[0][0], res[0][1], res[0][2])

    def getSecById(self, sec_id):
        sql = "SELECT ID, SYMBOL, DESCRIPTION FROM SECURITY WHERE ID='" + sec_id + "'"
        count = self.cur.execute(sql)
        if count == 0:
            return None
        res = self.cur.fetchall()
        return Security(res[0][0], res[0][1], res[0][2])

    def getOrCreateSec(self, symbol):
        sec = self.getSecBySym(symbol)
        if sec == None:
            self.createSecurity(symbol, '')
            sec = self.getSecBySym(symbol)
        return sec
        
    def insertHistory(self, history):
        N = len(history.times)                                                                              
        for i in range(N):
            sql = "INSERT INTO HISTORY_DAILY" + \
                "(SEC_ID, DATE, OPEN, HIGH, LOW, CLOSE, ADJ_CLOSE, VOLUME)" + \
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"                                                                       
            self.cur.execute(sql, (history.security.sec_id, history.times[i],
                                   history.opens[i], history.highs[i],
                                   history.lows[i], history.closes[i],
                                   history.adj_closes[i], history.volumes[i]))
    
    def getLastHistoryDate(self, sec):
        sql = "SELECT MAX(DATE) FROM HISTORY_DAILY WHERE SEC_ID=%s"
        count = self.cur.execute(sql, (sec.sec_id))
        if count == 0:
            return None
        res = self.cur.fetchall()
        return res[0][0]

    def getHistoryFrom(self, security, start):
        sql = "SELECT DATE, OPEN, HIGH, LOW, CLOSE, ADJ_CLOSE, VOLUME FROM HISTORY_DAILY WHERE SEC_ID=%s AND DATE>=%s ORDER BY DATE"
        count = self.cur.execute(sql, (security.sec_id, start))
        res = self.cur.fetchall()
        
        history = History(security)                                                         
        for i in range(count):                                                                    
            history.times.append(res[i][0])                        
            history.opens.append(float(res[i][1]))                                                  
            history.highs.append(float(res[i][2]))                                                  
            history.lows.append(float(res[i][3]))                                                   
            history.closes.append(float(res[i][4]))                                                 
            history.adj_closes.append(float(res[i][5]))                                             
            history.volumes.append(int(res[i][6]))                                                  

        if len(history.times) > 0 :
            history.start = history.times[0]
            history.end = history.times[len(history.times) - 1]
        else:
            history.start = None
            history.end = None

        return history                                    

    def updateHistory(self, sec):
        today = date.today()                                                                        
        yahoo = Yahoo()
        last = self.getLastHistoryDate(sec)
        if last == None:
            history = yahoo.fetch(sec)
            if history != None:
                self.insertHistory(history)
        elif today > last:
            from_date = last + timedelta(days=1)
            history = yahoo.fetch(sec, from_date, today)
            if history != None:
                self.insertHistory(history)


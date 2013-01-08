import urllib                                                                       
from datetime import datetime
from finlib import History

class Yahoo:                                                                                        
    def __init__(self):                                                                             
        self.proxies = {'http':'http://proxy-hbr-new.gslb.db.com:8080'}                            
        self.base_url = 'http://ichart.finance.yahoo.com/table.csv'                                 
                                                                                                    
    def download(self, symbol, start_date=None, end_date=None):     
        query = {}
        query['s'] = symbol
        if start_date != None:
            query['a'] = str(start_date.month - 1)
            query['b'] = str(start_date.day)
            query['c'] = str(start_date.year)
        if end_date != None:            
            query['d'] = str(end_date.month - 1)
            query['e'] = str(end_date.day)
            query['f'] = str(end_date.year)
        query['g'] = 'd'
        query['ignore'] = '.csv'
                                                                                                    
        data = urllib.urlencode(query)                      
        url = self.base_url + '?' + data
#        f = urllib.urlopen(url)                                                                     
        f = urllib.urlopen(url, proxies=self.proxies)                                              
        s = f.read()                                                                                
        f.close() 
        return s                                                                                    
                                                                                                    
    def fetch(self, security, start_date=None, end_date=None):   
        history = History(security, start_date, end_date)                                                         
        s = self.download(security.symbol, start_date, end_date)
        
        if s.startswith('<!doctype html'):
            return None
        
        lines = s.split('\n')                                                                 
        N = len(lines)                                                                              
        for i in range(1, N):                                                                       
            line = lines[N - i].strip()                                                             
            if len(line) == 0:                                                                      
                continue                                                                            
            fields = line.split(',')                                                                
            history.times.append(datetime.strptime(fields[0], '%Y-%m-%d'))                        
            history.opens.append(float(fields[1]))                                                  
            history.highs.append(float(fields[2]))                                                  
            history.lows.append(float(fields[3]))                                                   
            history.closes.append(float(fields[4]))                                                 
            history.volumes.append(int(fields[5]))                                                  
            history.adj_closes.append(float(fields[6]))                                             
                           
        history.start = history.times[0]
        history.end = history.times[len(history.times) - 1]

        return history                                    
    
    

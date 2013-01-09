import urllib                                                                       
from datetime import datetime

class Yahoo:                                                                                        
    def __init__(self, yahoo_url, http_proxy=None):
        self.base_url = yahoo_url
        self.http_proxy = http_proxy
                                                                                                    
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
        if self.http_proxy == None:
            f = urllib.urlopen(url)      
        else:                                                               
            f = urllib.urlopen(url, proxies={'http':self.http_proxy})                                              
        s = f.read()                                                                                
        f.close() 
        return s                                                                                    
                                                                                                    
    def fetch(self, security, start_date=None, end_date=None):   
        s = self.download(security['symbol'], start_date, end_date)
        
        if s.startswith('<!doctype html'):
            return None

        dates = []
        opens = []
        highs = []
        lows = []
        closes = []
        volumes = []
        adj_closes = []

        lines = s.split('\n')                                                                 
        N = len(lines)                                                                              
        for i in range(1, N):                                                                       
            line = lines[N - i].strip()                                                             
            if len(line) == 0:                                                                      
                continue                                                                            
            fields = line.split(',')                                                                
            dates.append(datetime.strptime(fields[0], '%Y-%m-%d'))                        
            opens.append(float(fields[1]))                                                  
            highs.append(float(fields[2]))                                                  
            lows.append(float(fields[3]))                                                   
            closes.append(float(fields[4]))                                                 
            volumes.append(int(fields[5]))                                                  
            adj_closes.append(float(fields[6]))                                             
                    
                    
        history = { 'dates':dates,
                   'opens':opens,
                   'highs':highs,
                   'lows':lows,
                   'closes':closes,
                   'volumes':volumes,
                   'adj_closes':adj_closes
                   }
                          
        return history                                    
    
    

import findb
from ConfigParser import SafeConfigParser
import logging
from datetime import date                                                                    
from datetime import datetime                                                                       
from datetime import timedelta                                                                      
import finlib


def plotThreeSMA(history, wdir):
    sec = history.security
                                                                         
    sma1 = finlib.sma(history.adj_closes, 7)                                                      
    sma2 = finlib.sma(history.adj_closes, 15)                                                     
    sma3 = finlib.sma(history.adj_closes, 30)                                                     
                                                                                                
    trend = 'flat'                                                                              
    last = len(sma1) - 1                                                                        
    if sma1[last] > sma2[last]  and sma2[last] > sma3[last]:                                    
        trend = 'up'                                                                            
    if sma1[last] < sma3[last] :                                                                
        trend = 'down'                                                                          
                                                                                                
    title = sec.desc[:25] + ' (' + sec.symbol + ') - ' + trend                                
    lines = [history.adj_closes, sma1, sma2, sma3]                                         
    labels = ['Close', 'SMA(7)', 'SMA(15)', 'SMA(30)' ]                                         
    name = sec.symbol + '-' + datetime.today().strftime('%Y%m%d')                                                                                       
                                                                                                
    chart = finlib.plot(title, history.times, lines, labels, 20, name, wdir)
    return chart                     
                                                                                                    
        
def main() :
    
    config_file = 'ma_rpr.ini'
    cfg = SafeConfigParser()
    cfg.read(config_file)

    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger("FinLib")
    logger.setLevel(logging.DEBUG)
    
    logger.info("starting..")

    db = findb.FinDB(cfg.get('db', 'server'), cfg.get('db', 'database'), cfg.get('db', 'user'), cfg.get('db', 'password'))
    db.connect()

    wdir = cfg.get('report', 'wdir')

    from_date = date.today() - timedelta(weeks=8)     
    charts = []

    symbols = cfg.get('report', 'symbols').strip().split(',')
    for symbol in symbols:
        symbol = symbol.strip()
        if len(symbol) == 0 :
            continue

        logger.info("loading " + symbol)
    
        sec = db.getOrCreateSec(symbol)
#        db.updateHistory(sec)
        history = db.getHistoryFrom(sec, from_date)
        if history.len() > 0:
            logger.info("generating chart for " + symbol)
            charts.append(plotThreeSMA(history, wdir))

    logger.info("sending the report")
    finlib.emailCharts(cfg.get('email', 'from'), cfg.get('email', 'to'),
                       'Todays Charts', charts, cfg.get('email', 'server'),
                       cfg.get('email', 'user'), cfg.get('email', 'passwd'))                                        
      
if __name__ == '__main__':
    main()

import finmdb
from yahoo import Yahoo                                                                      
from ConfigParser import SafeConfigParser
import logging
from datetime import datetime                                                                       
from datetime import timedelta                                                                      
import finlib


def plotThreeSMA(sec, history, wdir):
    
    adj_closes = []
    dates = []
    for h in history:
        adj_closes.append(h['adj_close'])
        dates.append(h['date'])
                                                                         
    sma1 = finlib.sma(adj_closes, 7)
    sma2 = finlib.sma(adj_closes, 15)
    sma3 = finlib.sma(adj_closes, 30)

    print dates
    print adj_closes
    print sma1
    print sma2
    print sma3

    trend = 'flat'                                                                              
    last = len(sma1) - 1                                                                        
    if sma1[last] > sma2[last]  and sma2[last] > sma3[last]:                                    
        trend = 'up'                                                                            
    if sma1[last] < sma3[last] :                                                                
        trend = 'down'                                                                          
                                                                                                
    title = sec['symbol'] + ' - ' + trend + ' (' + "{0:.2f}".format(sma3[last]) + ')'     
                         
    lines = [adj_closes, sma1, sma2, sma3]                                         
    labels = ['Close', 'SMA(7)', 'SMA(15)', 'SMA(30)' ]                                         
    name = sec['symbol'] + '-' + datetime.today().strftime('%Y%m%d')                                                                                       
                                                                                                
    chart = finlib.plot(title, dates, lines, labels, 20, name, wdir)
    return chart                     
                                                                                                    
        
def main() :
    
    config_file = 'ma_rpr.ini'
    cfg = SafeConfigParser()
    cfg.read(config_file)

    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger("FinLib")
    logger.setLevel(logging.DEBUG)
    
    logger.info("starting..")
    
    yahoo = Yahoo(cfg.get('report', 'yahoo_url'), cfg.get('report', 'http_proxy'))

    db = finmdb.FinMongoDB('localhost', 27017, 'findb', yahoo)
    db.connect()

    wdir = cfg.get('report', 'wdir')

    from_date = datetime.today() - timedelta(weeks=8)     
    charts = []

    symbols = cfg.get('report', 'symbols').strip().split(',')
    for symbol in symbols:
        symbol = symbol.strip()
        if len(symbol) == 0 :
            continue

        logger.info("loading " + symbol)
    
        sec = db.getOrCreateSec(symbol)
        db.updateHistory(sec)
        history = db.getHistoryFrom(sec, from_date)
        
        if history.count() > 0:
            logger.info("generating chart for " + symbol)
            charts.append(plotThreeSMA(sec, history, wdir))

    logger.info("sending the report")
    finlib.emailCharts(cfg.get('email', 'from'), cfg.get('email', 'to'),
                       'Todays Charts', charts, cfg.get('email', 'server'),
                       cfg.get('email', 'user'), cfg.get('email', 'passwd'))                                        
      
if __name__ == '__main__':
    main()

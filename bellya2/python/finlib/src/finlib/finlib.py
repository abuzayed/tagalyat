import matplotlib;matplotlib.use("Agg")                                                             
import matplotlib.pyplot as plt                                                                     
import matplotlib.ticker as ticker                                                                  

import smtplib                                                                                      
from email.MIMEMultipart import MIMEMultipart                                                       
from email.MIMEText import MIMEText                                                                 
from email.MIMEImage import MIMEImage                                                               

def sma(values, window):                                                                            
    sma = []                                                                                        
    total = 0                                                                                       
    for i in range(len(values)):                                                                    
        total = total + values[i]                                                                   
        if i < window:                                                                              
            sma.append(total / (i + 1))                                                             
        else:                                                                                       
            total = total - values[i - window]                                                      
            sma.append(total / window)                                                              
    return sma                                          

def plot(title, dates, lines, labels, count, name, wdir):
    
    N = len(dates)                                                                                  
    start = N - count                                                                               
    date_idx = range(count)                                                                         
                                                                                                    
    def format_date(x, pos=None):                                                                   
        idx = start + int(x)                                                                        
        if idx >= N:                                                                                
            idx = N - 1                                                                             
        return dates[idx].strftime('%m-%d')                                                         
                                                                                                    
    plt.rcParams.update({'font.size': 9})                                                           
    plt.rc('legend', **{'fontsize':8})                                                              
                                                                                                    
    fig = plt.figure()                                                                              
#    ax = fig.add_subplot(111)                                                                      
    ax = fig.add_axes([0.075, 0.125, 0.68, 0.765])                                                  
    handles = []                                                                                    
    for i in range(len(lines)):                                                                     
        handle = ax.plot(date_idx, lines[i][start:], label=labels[i])    
        handles.append(handle)                                                                      
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))                                 
                                                                                                    
    fig.autofmt_xdate()                                                                             
    fig.set_size_inches(4.25, 2.15)                                                                 
    fig.legend(handles, labels, 'upper right')                                                      
    plt.title(title)                                                                                
    
    filename = wdir + '\\' + name + '.png'                                                                                                              
#    plt.show()                                                                                     
    plt.savefig(filename)
    
    return (name, filename)                                                                     

def emailCharts(fromaddr, toaddrs, subject, charts, server, username, password):                                                          
    msgRoot = MIMEMultipart()   
    msgRoot['Subject'] = subject                                                                    
    msgRoot['From'] = fromaddr                                                                      
    msgRoot['To'] = toaddrs                                                                         
    msgRoot.preamble = subject                                                                      
    msgAlternative = MIMEMultipart('alternative')                                                   
    msgRoot.attach(msgAlternative)                                                                  
    msgText = MIMEText(subject)                                                                     
    msgAlternative.attach(msgText)                                                                  
    html = '<br>'                                                                                   
    for chart in charts:                                                                            
        html = html + '<img src="cid:' + chart[0] + '"><br>'                                  
                                                                                                    
    msgText = MIMEText(html, 'html')                                                                
    msgAlternative.attach(msgText)                                                                  
    for chart in charts:                                                                            
        fp = open(chart[1], 'rb')                                                             
        img = MIMEImage(fp.read())                                                                  
        fp.close()                                                                                  
        img.add_header('Content-ID', '<' + chart[0] + '>')                                    
        msgRoot.attach(img)                                                                         
                                                                                                    
    smtp = smtplib.SMTP(server)                                                       
    smtp.starttls()                                                                                 
    smtp.login(username, password)                                                                  
    smtp.sendmail(fromaddr, toaddrs, msgRoot.as_string())                                           
    smtp.quit() 

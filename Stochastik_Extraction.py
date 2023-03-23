import numpy as np
import requests


def requestStochastikIndikator(ticker, API_INFO, years=1):
    url = API_INFO.api_url + "function=STOCH" + "&symbol=" + str(ticker) + "&interval=daily" +API_INFO.api_key
    data = requests.get(url)
    data = data.json()
    
    data = data.get("Technical Analysis: STOCH")
    
    vals = list(data.values())
    dates = list(data.keys())

    vals = vals[0:(years*250)]
    dates = dates[0:(years*250)]
    
    slow_k = np.array([round(float(i.get('SlowK')),2) for i in vals])
    slow_d = np.array([round(float(i.get('SlowD')),2) for i in vals])
    
    dates = np.array(dates)
    dates = np.flip(dates)
    
    slow_k = np.flip(slow_k)
    slow_d = np.flip(slow_d)
    
    
    return (dates, slow_k, slow_d)


def getOversoldStochastik(y1,y2):
    maximum = np.max(y1)
    minimum = np.min(y1)

    vals = np.arange(minimum,maximum)

    lower = np.quantile(vals,0.1)
    res=[]
    for i in range(len(y1)):
        if(y1[i] < lower and y2[i] < lower):
            res.append(i)
    return res

def getOverboughtStochastik(y1,y2):
    maximum = np.max(y1)
    minimum = np.min(y1)

    vals = np.arange(minimum,maximum)

    upper = np.quantile(vals,0.9)
    res = []
    for i in range(len(y1)):
        if(y1[i] > upper and y2[i] > upper):
            res.append(i)
    return res


def single_thread_processing_stochastik(ticker, storage, API_INFO, storage_thread_lock):
    dates, slow_k, slow_d = requestStochastikIndikator(ticker, API_INFO)

    storage_thread_lock.acquire()
    storage['stoch']['values']['slow'] = slow_k
    storage['stoch']['values']['fast'] = slow_d
    storage_thread_lock.release()

    buy = getOversoldStochastik(slow_k, slow_d)
    sell = getOverboughtStochastik(slow_k, slow_d)

    storage_thread_lock.acquire()
    storage['stoch']['oversold'] = buy
    storage['stoch']['overbought'] = sell
    storage_thread_lock.release()
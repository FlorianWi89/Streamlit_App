import numpy as np
import requests



def requestMomentumIndikator(ticker, API_INFO, years=1):
    url = API_INFO.api_url + "function=MOM" + "&symbol=" + str(ticker) + "&interval=daily" + "&time_period=14" + "&series_type=close" +API_INFO.api_key
    data = requests.get(url)
    data = data.json()
    
    data = data.get("Technical Analysis: MOM")
    
    momentum = list(data.values())
    dates = list(data.keys())

    momentum = momentum[0:(years*250)]
    dates = dates[0:(years*250)]
    
    momentum = np.array([round(float(i.get('MOM')),2) for i in momentum])
    
    dates = np.array(dates)
    dates = np.flip(dates)
    
    momentum = np.flip(momentum)
    
    return (dates, momentum)


def getOversoldMomentum(mom):
    maximum = np.max(mom)
    minimum = np.min(mom)

    vals = np.arange(minimum,maximum)

    lower = np.quantile(vals,0.15)
    

    #list comprehension solution
    res = [i for i in range(len(mom)) if mom[i] <= lower]
    
    if len(res) <= 3:
        return res
    else:
        for i in range(0,len(res)-1):
            if res[i+1] - res[i] <= 2:
                res[i] = res[i+1]
                
        return list(set(res))

def getOverboughtMomentum(mom):
    maximum = np.max(mom)
    minimum = np.min(mom)

    vals = np.arange(minimum,maximum)

    upper = np.quantile(vals,0.85)
    
    res = [i for i in range(len(mom)) if mom[i] >= upper]
    
    if len(res) <= 3:
        return res
    else:
        for i in range(0,len(res)-1):
            if res[i+1] - res[i] <= 2:
                res[i] = res[i+1]
                
        return list(set(res))
    

def single_thread_processing_momentum(ticker, storage, API_INFO, storage_thread_lock):
    dates, mom = requestMomentumIndikator(ticker, API_INFO)

    storage_thread_lock.acquire()
    storage['mom']['values'] = mom
    storage_thread_lock.release()

    buy = getOversoldMomentum(mom)
    sell = getOverboughtMomentum(mom)

    storage_thread_lock.acquire()
    storage['mom']['oversold'] = buy
    storage['mom']['overbought'] = sell
    storage_thread_lock.release()

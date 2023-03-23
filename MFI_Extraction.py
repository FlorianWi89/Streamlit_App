import numpy as np
import requests



def requestMFIIndicator(ticker, API_INFO, years=1):
    url = API_INFO.api_url + "function=MFI" + "&symbol=" + str(ticker) + "&interval=daily" + "&time_period=14" + "&series_type=close" +API_INFO.api_key
    data = requests.get(url)
    data = data.json()
        
    data = data.get("Technical Analysis: MFI")

    mfi = list(data.values())
    dates = list(data.keys())

    mfi = mfi[0:(years*250)]
    dates = dates[0:(years*250)]
    
    mfi = np.array([round(float(i.get('MFI')),2) for i in mfi])
    dates = np.array(dates)

    mfi = np.flip(mfi)
    dates = np.flip(dates)
    
    return (dates, mfi)



def getOversoldMFI(mfi):
    bound = np.quantile((np.arange(np.min(mfi),np.max(mfi))),0.15)
    
    return [i for i in range(len(mfi)) if mfi[i] <= bound]

def getOverboughtMFI(mfi):
    bound = np.quantile((np.arange(np.min(mfi),np.max(mfi))),0.85)

    return [i for i in range(len(mfi)) if mfi[i] >= bound]


def single_thread_processing_mfi(ticker, storage, API_INFO, storage_thread_lock):
    dates, mfi = requestMFIIndicator(ticker, API_INFO)

    storage_thread_lock.acquire()
    storage['mfi']['values'] = mfi
    storage_thread_lock.release()

    buy = getOversoldMFI(mfi)
    sell = getOverboughtMFI(mfi)

    storage_thread_lock.acquire()
    storage['mfi']['oversold'] = buy
    storage['mfi']['overbought'] = sell
    storage_thread_lock.release()

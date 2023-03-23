import numpy as np
import pandas as pd
import requests
from scipy.signal import find_peaks,argrelmin



def requestTRIXIndicator(ticker, API_INFO, years=1, period=30):
    p = "&time_period={}".format(period)
    url = API_INFO.api_url + "function=TRIX" + "&symbol=" + str(ticker) + "&interval=daily" + p + "&series_type=close" +API_INFO.api_key
    data = requests.get(url)
    data = data.json()
    
    data = data.get("Technical Analysis: TRIX")

    trix = list(data.values())
    dates = list(data.keys())

    trix = trix[0:(years*250)]
    dates = dates[0:(years*250)]

    trix = np.array([round(float(i.get('TRIX')),2) for i in trix])
    
    dates = np.array(dates)
    dates = np.flip(dates)
    
    trix = np.flip(trix)
    
    return (dates, trix)
    


def getOversoldTrix(vals):
    vals = [-x for x in vals]
    peaks, _ = find_peaks(vals)
    return peaks

def getOverboughtTrix(vals):
    peaks, _ = find_peaks(vals)
    return peaks


def single_thread_processing_trix(ticker, storage, API_INFO, storage_thread_lock):
    dates, trix = requestTRIXIndicator(ticker, API_INFO)

    storage_thread_lock.acquire()
    storage['trix']['values'] = trix
    storage_thread_lock.release()

    buy = getOversoldTrix(trix)
    sell = getOverboughtTrix(trix)

    storage_thread_lock.acquire()
    storage['trix']['oversold'] = buy
    storage['trix']['overbought'] = sell
    storage_thread_lock.release()

import numpy as np
import requests



def requestRSIIndicator(ticker, API_INFO, years=1):
    url = API_INFO.api_url + "function=RSI" + "&symbol=" + str(ticker) + "&interval=daily" + "&time_period=14" + "&series_type=close" +API_INFO.api_key
    data = requests.get(url)
    data = data.json()
    
    data = data.get("Technical Analysis: RSI")
    
    rsi = list(data.values())
    dates = list(data.keys())

    rsi = rsi[0:(years*250)]
    dates = dates[0:(years*250)]
    
    rsi = np.array([round(float(i.get('RSI')),2) for i in rsi])
    dates = np.array(dates)

    rsi = np.flip(rsi)
    dates = np.flip(dates)
    
    return (dates, rsi)


def getOversoldRSI(rsi_vals):
    
    bound = np.quantile((np.arange(np.min(rsi_vals),np.max(rsi_vals))),0.15)
    
    return [i for i in range(len(rsi_vals)) if rsi_vals[i] <= bound]

def getOverboughtRSI(rsi_vals):
    bound = np.quantile((np.arange(np.min(rsi_vals),np.max(rsi_vals))),0.85)
    return [i for i in range(len(rsi_vals)) if rsi_vals[i] >= bound]


def single_thread_processing_rsi(ticker, storage, API_INFO, storage_thread_lock):
    dates, rsi = requestRSIIndicator(ticker, API_INFO)

    storage_thread_lock.acquire()
    storage['rsi']['values'] = rsi
    storage_thread_lock.release()

    buy = getOversoldRSI(rsi)
    sell = getOverboughtRSI(rsi)

    storage_thread_lock.acquire()
    storage['rsi']['oversold'] = buy
    storage['rsi']['overbought'] = sell
    storage_thread_lock.release()
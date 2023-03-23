import numpy as np
import requests

def requestMACDIndicator(ticker, API_INFO, years=1):
    url = API_INFO.api_url + "function=MACD" + "&symbol=" + str(ticker) + "&interval=daily" + "&series_type=close" +API_INFO.api_key
    data = requests.get(url)
    data = data.json()
    
    data = data.get("Technical Analysis: MACD")
    
    macd = list(data.values())
    dates = list(data.keys())

    macd = macd[0:(years*250)]
    dates = dates[0:(years*250)]
    
    macd_values = np.array([round(float(i.get('MACD')),2) for i in macd]) 
    macd_signal = np.array([round(float(i.get('MACD_Signal')),2) for i in macd])
    macd_hist = np.array([round(float(i.get('MACD_Hist')),2) for i in macd])
    
    dates = np.array(dates)
    dates = np.flip(dates)
    
    macd_values = np.flip(macd_values)
    macd_signal = np.flip(macd_signal)
    macd_hist = np.flip(macd_hist)
    
    
    return (dates, macd_values, macd_signal, macd_hist)


def getCrossMACD(macd_signal,macd_values):
                
    #set marker lines

    maximum = np.max(macd_signal)
    minimum = np.min(macd_signal)

    vals = np.arange(minimum,maximum)

    upper = np.quantile(vals,0.8)
    lower = np.quantile(vals,0.2)
    
    idx = np.argwhere(np.diff(np.sign(np.array(macd_signal) - np.array(macd_values)))).flatten()

    
    up_cross = [i for i in idx if macd_signal[i] < lower]
    down_cross = [i for i in idx if macd_signal[i] > upper]

    buy_signal =  up_cross
    sell_signal = down_cross
            
    return (buy_signal, sell_signal)


def single_thread_processing_macd(ticker, storage, API_INFO, storage_thread_lock):
    dates, values, signals, hist = requestMACDIndicator(ticker, API_INFO)
    storage_thread_lock.acquire()
    storage['macd']['values']['values'] = values
    storage['macd']['values']['signals'] = signals
    storage_thread_lock.release()
    buy,sell = getCrossMACD(signals, values)
    storage_thread_lock.acquire()
    storage['macd']['signal']['oversold'] = buy
    storage['macd']['signal']['overbought'] = sell
    storage_thread_lock.release()




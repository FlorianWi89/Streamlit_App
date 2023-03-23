import numpy as np
import requests

#function to request daily adjusted historical time series data
def requestDailyAdjusted(ticker, API_INFO, years=1):
    url = API_INFO.api_url + "function=TIME_SERIES_DAILY_ADJUSTED" + "&symbol=" + str(ticker) + "&outputsize=full" +API_INFO.api_key
    data = requests.get(url)
    data = data.json()
    
    data = data.get("Time Series (Daily)")
    
    prices = list(data.values())
    dates = list(data.keys())
    
    prices = prices[0:(years*250)]
    dates = dates[0:(years*250)]
    
    prices = np.array([round(float(i.get('5. adjusted close')),2) for i in prices])
    dates = np.array(dates)
    
    prices = np.flip(prices)
    dates = np.flip(dates)
    
    return (dates, prices)


#function to request daily adjusted historical time series data
def requestWeeklyAdjusted(ticker, API_INFO, years=1):
    url = API_INFO.api_url + "function=TIME_SERIES_WEEKLY_ADJUSTED" + "&symbol=" + str(ticker) +API_INFO.api_key
    data = requests.get(url)
    data = data.json()
    
    data = data.get("Weekly Adjusted Time Series")
    
    prices = list(data.values())
    dates = list(data.keys())
    
    prices = prices[0:(years*52)]
    dates = dates[0:(years*52)]
    
    prices = np.array([round(float(i.get('5. adjusted close')),2) for i in prices])
    dates = np.array(dates)
    
    prices = np.flip(prices)
    dates = np.flip(dates)
    
    return (dates, prices)
    
def single_thread_processing_chart(ticker, storage, API_INFO, storage_thread_lock):
    dates, prices = requestDailyAdjusted(ticker, API_INFO)

    storage_thread_lock.acquire()
    storage['chart'] = prices
    storage_thread_lock.release()

    
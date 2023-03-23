
import numpy as np
import pandas as pd
import requests


def requestMA(ticker, period=50,ma_type="W"):
    url = API_URL + "function={}MA".format(ma_type) + "&symbol=" + str(ticker) + "&interval=daily" + "&time_period="+str(period) + "&series_type=close" +API_KEY
    data = requests.get(url)
    data = data.json()
    
    data = data.get("Technical Analysis: {}MA".format(ma_type))
    
    vals = data.values()
    dates = list(data.keys())
    
    ma = np.array([round(float(i.get('{}MA'.format(ma_type))),2) for i in vals])
    dates = np.array(dates)
    
    dates = np.flip(dates)
    ma = np.flip(ma)
    
    
    return (dates, ma)

def getNYearMA(dates,ma, period=1):
    dates = list(dates)
    ma = list(ma)

    return (dates[period *(-250):],ma[period * (-250):])


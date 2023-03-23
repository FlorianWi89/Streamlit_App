#!/usr/bin/env python
# coding: utf-8

import numpy as np
import time
import matplotlib.pyplot as plt
from Chart_Data_Extraction import requestDailyAdjusted

def plotWithSignals(chart,buy,sell,title=""):
    plt.rcParams["figure.figsize"] = (15,3)
    plt.plot(chart)
    for i in sell:
        plt.axvline(x = i, color = 'r', label = 'axvline - full height')
    for i in buy:
        plt.axvline(x = i, color = 'g', label = 'axvline - full height')
    plt.title(title)
    plt.show()
    
class ApiInformation():
    def __init__(self,key,url):
        self.api_key = key
        self.api_url = url

class ThreadInformation():
    def __init__(self, storage_lock):
        self.storage_lock = storage_lock


def item_batcher(number_of_batches, number_of_items):
    lst = range(number_of_items)
    return np.array_split(lst,number_of_batches)


#function to batch symbols for requesting. Considering the max 100 calls per min
def list_batcher(data, threads):
    #create batches for every thread
    x = np.array_split(data, threads) 
    #create batches for every minute for a thread
    return list(map(lambda e : np.array_split(e,np.ceil(len(e)/100)),x))



def getCombinedMomentumSignals(macd_signal,rsi,mom,stoch, length):
    signals = []
    for idx in range(2,length,5):
        v = [x for x in range(idx - 2, idx + 3)] #create window
        a = len(list(set(v).intersection(set(macd_signal))))
        b = len(list(set(v).intersection(set(rsi))))
        c = len(list(set(v).intersection(set(mom))))
        d = len(list(set(v).intersection(set(stoch))))
            
        if (a+b+c+d) > 2:
            signals.append(max(v))     
    return signals


def chart_data_requesting(T_id, tickers,storage,API_INFO, Thread_INFO):
    for idx in range(len(tickers)):
        for ticker in tickers[idx]:
            try:
                d,p = requestDailyAdjusted(ticker, API_INFO)

                if len(p) != 250:
                    continue

                Thread_INFO.storage_lock.acquire()
                storage[ticker] = p
                Thread_INFO.storage_lock.release()
            
            except Exception as e:
                print(e)
    
        if len(tickers) != 1 or idx != len(tickers)-1:
            print("Thread {} sleeping...".format(T_id))
            time.sleep(30)


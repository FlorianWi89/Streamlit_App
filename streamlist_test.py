import streamlit as st
import matplotlib.pyplot as plt
from Chart_Data_Extraction import requestDailyAdjusted
from RSI_Extraction import requestRSIIndicator, getOverboughtRSI, getOversoldRSI
from Momentum_Extraction import requestMomentumIndikator, getOverboughtMomentum, getOversoldMomentum
from Stochastik_Extraction import requestStochastikIndikator, getOverboughtStochastik, getOversoldStochastik
from MACD_Extraction import requestMACDIndicator, getCrossMACD
from MFI_Extraction import requestMFIIndicator, getOverboughtMFI, getOversoldMFI
from utils import plotWithSignals

class ApiInformation():
    def __init__(self,key,url):
        self.api_key = key
        self.api_url = url


API_KEY = "&apikey=94VAKAGALC5KMWMV"
API_URL = "https://www.alphavantage.co/query?"

API_INFO = ApiInformation(API_KEY,API_URL)

storage = {
    'chart' : [], 
    'macd' : {'values' : {'values' : [], 'signals' : []}, 'signal' :{ 'oversold' : [], 'overbought' : []}}, 
    'rsi' : {'values' : [], 'oversold' : [], 'overbought' : []}, 
    'mom' : {'values' : [], 'oversold' : [], 'overbought' : []},
    'mfi' : {'values' : [], 'oversold' : [], 'overbought' : []},
    'stoch' : {'values' : {'slow' : [], 'fast' : []}, 'oversold' : [], 'overbought' : []}
}

def process_data():
    _, values = requestDailyAdjusted(ticker, API_INFO, years)
    storage['chart'] = values
    

def request_selected_indicators():
    for i in range(len(indicators)):
        if indicators[i] == 'RSI':
            _, rsi = requestRSIIndicator(ticker, API_INFO)
            storage['rsi']['values'] = rsi
            buy = getOversoldRSI(rsi)
            sell = getOverboughtRSI(rsi)
            storage['rsi']['oversold'] = buy
            storage['rsi']['overbought'] = sell

        if indicators[i] == 'MACD':
            _, values, signals, _ = requestMACDIndicator(ticker, API_INFO)
            storage['macd']['values']['values'] = values
            storage['macd']['values']['signals'] = signals
            buy,sell = getCrossMACD(signals, values)
            storage['macd']['signal']['oversold'] = buy
            storage['macd']['signal']['overbought'] = sell

        if indicators[i] == 'MFI':
            _, mfi = requestMFIIndicator(ticker, API_INFO)
            storage['mfi']['values'] = mfi
            buy = getOversoldMFI(mfi)
            sell = getOverboughtMFI(mfi)
            storage['mfi']['oversold'] = buy
            storage['mfi']['overbought'] = sell

        if indicators[i] == 'Stochastik':
            _, slow_k, slow_d = requestStochastikIndikator(ticker, API_INFO)
            storage['stoch']['values']['slow'] = slow_k
            storage['stoch']['values']['fast'] = slow_d
            buy = getOversoldStochastik(slow_k, slow_d)
            sell = getOverboughtStochastik(slow_k, slow_d)
            storage['stoch']['oversold'] = buy
            storage['stoch']['overbought'] = sell

        if indicators[i] == 'Momentum':
            _, mom = requestMomentumIndikator(ticker, API_INFO)
            storage['mom']['values'] = mom
            buy = getOversoldMomentum(mom)
            sell = getOverboughtMomentum(mom)
            storage['mom']['oversold'] = buy
            storage['mom']['overbought'] = sell



with st.sidebar:
    st.title("Stock Analyser")
    st.subheader("By Wicher Investment Corp.")
    ticker = st.text_input(label="Type in the Ticker Symbol (NYSE,XETRA) of your stock:")
    
    indicators = st.multiselect(label="Select the indicators you want to analyse:",
                    options=['RSI','MACD','MFI','Stochastik','Momentum'])
    
    years = st.number_input(label="Enter the number of years you want to view", min_value=1,max_value=5,step=1)
    if st.button(label="Request Data",use_container_width=True):
        user_response = st.text("Requesting data")
        process_data()
        if len(indicators) != 0:
           request_selected_indicators()
        user_response = st.text("Processing data")

with st.container():
   
    if len(storage['chart']) != 0:
        st.write("Chart of ",ticker)
        fig = plt.figure(figsize=(13,3))
        plt.plot(storage['chart'])
        st.pyplot(fig)

    if len(storage['rsi']['values']) != 0:
        st.write("Relative Strength Indicator")   
        fig = plt.figure(figsize=(13,3))
        plt.plot(storage['rsi']['values'])
        for i in storage['rsi']['overbought']:
            plt.axvline(x = i, color = 'r', label = 'axvline - full height')
        for i in storage['rsi']['oversold']:
            plt.axvline(x = i, color = 'g', label = 'axvline - full height')
        st.pyplot(fig)

    if len(storage['mom']['values']) != 0:
        st.write("Momentum Indicator")   
        fig = plt.figure(figsize=(13,3))
        plt.plot(storage['mom']['values'])
        for i in storage['mom']['overbought']:
            plt.axvline(x = i, color = 'r', label = 'axvline - full height')
        for i in storage['mom']['oversold']:
            plt.axvline(x = i, color = 'g', label = 'axvline - full height')
        st.pyplot(fig)

    if len(storage['mfi']['values']) != 0:
        st.write("Money Flow Indicator")   
        fig = plt.figure(figsize=(13,3))
        plt.plot(storage['mfi']['values'])
        for i in storage['mfi']['overbought']:
            plt.axvline(x = i, color = 'r', label = 'axvline - full height')
        for i in storage['mfi']['oversold']:
            plt.axvline(x = i, color = 'g', label = 'axvline - full height')
        st.pyplot(fig)

    if len(storage['stoch']['values']['slow']) != 0:
        st.write("Stochastik Indicator")   
        fig = plt.figure(figsize=(13,3))
        plt.plot(storage['stoch']['values']['slow'])
        plt.plot(storage['stoch']['values']['fast'])
        for i in storage['stoch']['overbought']:
            plt.axvline(x = i, color = 'r', label = 'axvline - full height')
        for i in storage['stoch']['oversold']:
            plt.axvline(x = i, color = 'g', label = 'axvline - full height')
        st.pyplot(fig)


    if len(storage['macd']['values']['values']) != 0:
        st.write("Moving Average Convergence/Divergence Indicator")   
        fig = plt.figure(figsize=(13,3))
        plt.plot(storage['macd']['values']['values'])
        plt.plot(storage['macd']['values']['signals'])

        for i in storage['macd']['signal']['overbought']:
            plt.axvline(x = i, color = 'r', label = 'axvline - full height')
        for i in storage['macd']['signal']['oversold']:
            plt.axvline(x = i, color = 'g', label = 'axvline - full height')
        st.pyplot(fig)


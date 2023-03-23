import threading
from Chart_Data_Extraction import requestDailyAdjusted

class WorkerThread(threading.Thread):
    def __init__(self, thread_ID, thread_name, API_INFO, tickers, storage):
        threading.Thread.__init__(self)
        
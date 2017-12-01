import time
import requests
import json
import multiprocessing
import signal

class BitcoinPriceGetter(multiprocessing.Process):
    def __init__(self):
        super(BitcoinPriceGetter, self).__init__()

    def GetBitCoinPrice(self):
        rate = requests.get("https://coincheck.com/api/rate/btc_jpy")   # use public API of coincheck.com
        price_str = rate.json()['rate']
        price_int = int(float(price_str))
        return price_int    # currency is japanese yen

    def run(self, price, stop_flag):
        signal.signal(signal.SIGINT,  signal.SIG_IGN)
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        # get bitcoin price 0.5s periods
        while(1):
            if stop_flag.is_set() :
                break
            price.value = self.GetBitCoinPrice()
            time.sleep(0.5)

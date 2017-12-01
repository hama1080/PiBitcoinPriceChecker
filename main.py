from DisplayController import DisplayController
from BitcoinPriceGetter import BitcoinPriceGetter
from multiprocessing import Value, Process, Event
import signal

def signalHandler(signal, handler) :
    stop_flag.set()

if __name__ == "__main__":
    print("start program")
    price_value = Value('i',0)
    stop_flag = Event()

    job_7seg = DisplayController()
    job_bitcoin = BitcoinPriceGetter()

    process_7seg = Process(target = job_7seg.run, args = (price_value, stop_flag))
    process_bitcoin = Process(target = job_bitcoin.run, args = (price_value, stop_flag))

    process_7seg.start()
    process_bitcoin.start()

    signal.signal(signal.SIGINT,  signalHandler)
    signal.signal(signal.SIGTERM, signalHandler)

    process_7seg.join()
    process_bitcoin.join()

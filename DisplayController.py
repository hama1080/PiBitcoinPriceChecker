import RPi.GPIO as GPIO
import time
import multiprocessing
from enum import Enum
import signal

# Use cathode common 7-segment led.
# number of 7-segment led: 8
# GPIO 2~9: led anode(d0~d7)
# GPIO 10~17: cathode(A~G+DP)

class DigitNum(Enum):
    D0 = 2
    D1 = 3
    D2 = 4
    D3 = 5
    D4 = 6
    D5 = 7
    D6 = 8
    D7 = 9

class Segment(Enum):
    A = 10
    B = 11
    C = 12
    D = 13
    E = 14
    F = 15
    G = 16
    DP = 17

DigitList = [DigitNum.D0, DigitNum.D1, DigitNum.D2, DigitNum.D3, DigitNum.D4, DigitNum.D5, DigitNum.D6, DigitNum.D7]

NumberDefinition = {
    " " : [],
    "0" : [Segment.A, Segment.B, Segment.C, Segment.D, Segment.E, Segment.F],
    "1" : [Segment.B, Segment.C],
    "2" : [Segment.A, Segment.B, Segment.D, Segment.E, Segment.G],
    "3" : [Segment.A, Segment.B, Segment.C, Segment.D, Segment.G],
    "4" : [Segment.B, Segment.C, Segment.F, Segment.G],
    "5" : [Segment.A, Segment.C, Segment.D, Segment.F, Segment.G],
    "6" : [Segment.A, Segment.C, Segment.D, Segment.E, Segment.F, Segment.G],
    "7" : [Segment.A, Segment.B, Segment.C, Segment.F],
    "8" : [Segment.A, Segment.B, Segment.C, Segment.D, Segment.E, Segment.F, Segment.G],
    "9" : [Segment.A, Segment.B, Segment.C, Segment.D, Segment.F, Segment.G]
}

class DisplayController(multiprocessing.Process):
    def __init__(self):
        super(DisplayController, self).__init__()

    def InitializeIO(self):
        GPIO.setmode(GPIO.BCM)
        for i in range(2, 18):
            GPIO.setup(i, GPIO.OUT)
        for i in range(10, 18):
            GPIO.output(i, 1)

    def ResetOutput(self):
        for i in range(2, 18):
            GPIO.output(i, 0)

    # num: str "00000000" ~ "99999999"
    # use dynamic lighting system
    def DisplayNumber(self, num_str):
        digit_cnt = 0
        for digit in DigitList:
            # turn on anode
            GPIO.output(digit.value, 1)
            digit_char = num_str[digit_cnt]

            # turn on cathode
            for i in NumberDefinition[digit_char]:
                GPIO.output(i.value, 0)

            # wait, should adjust sleep time to light clearly
            time.sleep(0.002)

            # turn off cathode
            for i in range(10, 18):
                GPIO.output(i, 1)

            # turn off anode
            GPIO.output(digit.value, 0)
            digit_cnt+=1

    def run(self, price, stop_flag):
        signal.signal(signal.SIGINT,  signal.SIG_IGN)
        signal.signal(signal.SIGTERM, signal.SIG_IGN)

        self.InitializeIO()
        while(1):
            if stop_flag.is_set() :
                self.ResetOutput()
                GPIO.cleanup()
                break
            cnt_padded = '{0:8d}'.format(price.value)
            self.DisplayNumber(cnt_padded)

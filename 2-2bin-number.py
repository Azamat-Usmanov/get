import RPi.GPIO as asd
import time

asd.setmode(asd.BCM)
dac = [10, 9, 11, 5, 6, 13, 19, 26]
number = [1, 1, 1, 1, 1, 1, 1, 1]

asd.setup(dac, asd.OUT)
asd.output(dac, number)
time.sleep(13)
asd.output(dac, 0)
asd.cleanup()

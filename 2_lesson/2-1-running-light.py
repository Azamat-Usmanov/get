import RPi.GPIO as asd
import time 

asd.setmode(asd.BCM)
leds = [24, 25, 8, 7, 12, 16, 20, 21]
asd.setup(leds, asd.OUT)
for i in range(3):
    for j in leds[::-1]:
        asd.output(j, 1)
        time.sleep(0.2)
        asd.output(j, 0)
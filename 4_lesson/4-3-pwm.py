import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT, initial = 0)

p = GPIO.PWM(24, 1000)

def ChangeDutyCycle(dutycycle):
    p.start(dutycycle)

try:
    while True:
        inputSt = input("Enter number from 0 to 100, 'q' for quit: ")

        if inputSt.isdigit():
            dutycycle = int(inputSt)
            if dutycycle > 100:
                print("Error")
                continue
            ChangeDutyCycle(dutycycle)
            print(str(3.3 * dutycycle/100) + " V")
        elif inputSt == 'q':
            break
        else:
            print("Error")
finally:
    p.stop()
    GPIO.cleanup()
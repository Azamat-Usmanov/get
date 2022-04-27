import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
comp = 4
troyka = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec2bin(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

def bin2dec(value):
    dec = 0
    deg = 0
    for i in range(7, -1, -1):
        dec += (2*value[i])**deg
        deg += 1
    return dec

def adc():
    bin = dec2bin(0)
    for i in range(8):
        bin[i] = 1
        GPIO.output(dac, bin)
        GPIO.output(leds, bin)
        time.sleep(0.001)
        if GPIO.input(comp) == 0:
            bin[i] = 0

    dec = bin2dec(bin)
    return dec

try:
    all_values = list()
    start_time = time.time() # Начало эксперемента

    volt = (3.3 * adc()) /256
    GPIO.output(troyka, 1) # Подаем 3.3 вольта на вход тройки модуля
    while volt < (0.97 * 3.3):
        all_values.append(volt)
        print(f"{volt} V")
        time.sleep(0.05)
        volt = (3.3 * adc()) / 256 # Измеряем напряжение на конденсаторе

    GPIO.output(troyka, 0) # Подаем 0 вольт на вход тройки модуля
    while volt > (0.02 * 3.3):
        all_values.append(volt)
        print(f"{volt} V")
        time.sleep(0.05)
        volt = (3.3 * adc()) / 256 # Измеряем напряжение на конденсаторе

    end_time = time.time() # Конец эксперемента

    total_time = end_time - start_time # Продолжительность эксперемента

    str_value = [str(item) for item in all_values]
    frq = len(all_values) / total_time
    period = total_time / len(all_values)
    step = (max(all_values) - min(all_values)) / 256
    frq_step = [frq, step] # Средняя частота дискритизации

    with open("data.txt", "w") as file: # Запись в файл
        file.write("\n".join(str_value))

    with open("settings.txt", "w") as file: 
        file.write("\n".join([str(item) for item in frq_step]))

    print(f"Total Time: {total_time}\nPeriod: {period}\nFrequency: {frq}\nStep: {step}") # Вывод в терминал

    plt.plot(all_values) # Построим график
    plt.show()

finally:
    GPIO.output(leds, 0)
    GPIO.output(dac, 0)
    GPIO.cleanup()
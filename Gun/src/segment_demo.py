import machine

clockPin = machine.Pin(12, machine.Pin.OUT)
dataPin = machine.Pin(14, machine.Pin.OUT)


def shift_update(input, data, clock):
    # load data in reverse order
    for i in range(7, -1, -1):
        clockPin.value(0)
        dataPin.value(int(input[i]))
        clockPin.value(1)

    clockPin.value(0)


numbDict = {
    "0": "11010111",
    "1": "00010001",
    "2": "11001011",
    "3": "01011011",
    "4": "00011101",
    "5": "01011110",
    "6": "11011110",
    "7": "00010011",
    "8": "11011111",
    "9": "01011111",
}

while True:
    for i in range(10):
        shift_update(numbDict[f"{i}"], data=dataPin, clock=clockPin)
        time.sleep(0.3)


# 1: links onder
# 2: onder
# 3: punt
# 4: rechts onder
# 5: mid
# 6: links boven
# 7: boven
# 8: rechts boven
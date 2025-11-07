import time
import board
import digitalio
import adafruit_dht
from datetime import datetime
import csv

sensor = adafruit_dht.DHT11(board.D16) # Change the pin number to the data pin of your DHT11
red = digitalio.DigitalInOut(board.D12)
blue = digitalio.DigitalInOut(board.D21)
red.direction = digitalio.Direction.OUTPUT
blue.direction = digitalio.Direction.OUTPUT
print("time,celsius,fahrenheit")

def to_fahrenheit(c):
    # TODO: Assign f where f represents the Farienheit equivalent to the input Celcius c
    f = celsius * (9/5) + 32
    return f
while True:
    try:
        celsius = sensor.temperature # Get the temperature in Celcius from the sensor
        fahrenheit = to_fahrenheit(celsius)
        current_time = datetime.now()
        with open('temperature.csv', 'a') as temperature: 
            writer = csv.writer(temperature)
            writer.writerow(["{0},{1:0.1f},{2:0.1f}".format(current_time.strftime("%H:%M:%S"), celsius, fahrenheit)])

        # TODO: Light up the red light when the temperature is above 72, and blue when it is below 72.
        if fahrenheit >= 72:
            red.value = True
            time.sleep(1)
            red.value = False
        elif fahrenheit < 72:
            blue.value = True
            time.sleep(1)
            blue.value = False
        time.sleep(1.0)
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except KeyboardInterrupt:
        GPIO.cleanup()
    except Exception as error:
        sensor.exit()
        raise error

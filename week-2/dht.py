import serial
import time

# Setup serial connection
s = serial.Serial('COM10', 9600)
time.sleep(2)

with open("dht22_data.csv", "a") as file:
    while True:
        line = s.readline().decode().strip()
        if line:
            timestamp = time.strftime('%Y%m%d%H%M%S')
            file.write(f"{timestamp},{line}\n")
            print(f"{timestamp},{line}")

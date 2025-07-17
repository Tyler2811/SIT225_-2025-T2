import serial
import random
import time
from datetime import datetime

baud_rate = 9600

s = serial.Serial('COM10', baud_rate, timeout=5)
time.sleep(2) 

while True:
    blink_count = random.randint(1, 5)
    s.write(bytes(str(blink_count) + '\n', 'utf-8'))
    send_time = datetime.now().strftime("%H:%M:%S")
    print(f"[{send_time}] Send -> {blink_count}")

    response = s.readline().decode('utf-8').strip()
    receive_time = datetime.now().strftime("%H:%M:%S")
    print(f"[{receive_time}] Receive <- {response}")

    try:
        sleep_time = int(response)
        time.sleep(sleep_time)
        receive_time = datetime.now().strftime("%H:%M:%S")
        print(f"[{receive_time}] Sleeping is done.\n")
    except ValueError:
        print("No response from Arduino\n")

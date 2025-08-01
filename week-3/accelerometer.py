import serial
from datetime import datetime

SERIAL_PORT = 'COM10'      
CSV_FILE = 'accel_data.csv'
# Open serial port
s = serial.Serial(SERIAL_PORT, 9600, timeout=1)
print("Logging started. Press Ctrl+C to stop.")

with open(CSV_FILE, 'a') as file:
    while True:
        try:
            line = s.readline().decode().strip()
            if line:
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                file.write(f"{timestamp},{line}\n")
                print(f"{timestamp},{line}")
        except KeyboardInterrupt:
            print("Logging stopped by user.")
            break
        except Exception as e:
            print("Error:", e)

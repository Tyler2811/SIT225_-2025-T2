import serial
from datetime import datetime

PORT = 'COM10'   # Change to your port
BAUD = 9600
FILE = 'accel_log.csv'

ser = serial.Serial(PORT, BAUD, timeout=1)

# Write CSV header
with open(FILE, 'w') as f:
    f.write("timestamp,accMagnitude,alarmLED\n")

print("Logging started... Press Ctrl+C to stop.")
try:
    while True:
        line = ser.readline().decode().strip()
        if line:
            try:
                mag_str = line.split(",")[-1]  # last value from Arduino print
                magnitude = float(mag_str)
                alarm = int(magnitude > 1.5)  # 1 if over threshold
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(FILE, 'a') as f:
                    f.write(f"{ts},{magnitude:.2f},{alarm}\n")
                print(f"{ts} | Mag:{magnitude:.2f} Alarm:{alarm}")
            except ValueError:
                pass
except KeyboardInterrupt:
    print("Logging stopped.")

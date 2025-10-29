import serial
import csv
import time
import os
from plotting import *
from datetime import datetime

# Config
SERIAL_PORT = 'COM7'
BAUD_RATE = 115200
LOG_TIME = 5  # in seconds
SAVE_PATH = 'logs'
PLOT = False

#--------------------
os.makedirs(SAVE_PATH, exist_ok=True)
filename = os.path.join(SAVE_PATH, f"sensor_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

ser = serial.Serial(SERIAL_PORT, BAUD_RATE) 
start_time = time.time()

with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Time', 'delta_X', 'delta_Y'])
    print(f"logging for {LOG_TIME}s")

    try:
        while (time.time() - start_time) < LOG_TIME:
            line = ser.readline().decode(errors='ignore').strip()
            if line:
                values = line.split(',')
                timestamp = datetime.now().strftime('%H:%M:%S.%f')
                writer.writerow([timestamp] + values)
    finally: 
        ser.close()
        print(f"\n Finished. File : {filename}")
        if PLOT:
            time.sleep(0.2)
            filename = filename.replace(os.sep, '/')
            plot_hist(filename)
            plot_path(filename)
            print(filename)

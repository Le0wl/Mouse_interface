import serial
import csv
import time
import os
from plotting import *
from datetime import datetime
import pandas as pd
# current problems: takes 2 seconds to come start reading?

# Config
SERIAL_PORT = 'COM7'
BAUD_RATE = 500000 #115200
LOG_TIME = 5  # in seconds
SAVE_PATH = 'logs'
PLOT = True

#--------------------
os.makedirs(SAVE_PATH, exist_ok=True)
filename = os.path.join(SAVE_PATH, f"sensor_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

ser = serial.Serial(SERIAL_PORT, BAUD_RATE) 
for _ in range(10):  # trying to fix the inital data being funny
    ser.readline()
start_time = time.time()

with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Time', 'contact','delta_X', 'delta_Y'])
    print(f"logging for {LOG_TIME}s")

    try:
        while (time.time() - start_time) < LOG_TIME:
            line = ser.readline().decode(errors='ignore').strip()
            if line:
                values = line.split(',')
                writer.writerow( values)
    finally: 
        ser.close()

df = pd.read_csv(filename)
df = df.fillna(0)
start_arduino = pd.to_numeric(df['Time'].iloc[0])
df["Time"] = datetime.fromtimestamp(start_time) + pd.to_timedelta(df["Time"] - start_arduino, unit="us")
df.to_csv(filename)
print(f"\n Finished. File : {filename}")

if PLOT:
    plot_hist(filename)
    print(filename)

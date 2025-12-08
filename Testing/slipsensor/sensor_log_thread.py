import csv, time, serial
import pandas as pd
from datetime import datetime
from config import *



# # data logging thread no longer used
# def log_slip(stop_event, log_ready_event, filename, timing, timing_lock):
#     try:
#         ser = serial.Serial(ARDUINO_PORT['slip'], BAUD_RATE['slip'])
#         for _ in range(10):
#             ser.readline()  # flush the buffer
#         with timing_lock:
#             timing['start_time'] = time.time()

#         with open(filename, 'w', newline='') as csvfile:
#             writer = csv.writer(csvfile)
#             writer.writerow(['Timestamp','Time', 'contact', 'delta_X', 'delta_Y','Movement'])
#             print(f"Mouse Logging started for {LOG_TIME}s")
#             log_ready_event.set()
#             with timing_lock:
#                 timing['start_log'] = datetime.now()
#             try:
#                 while (not stop_event.is_set()) and ((time.time() - timing['start_time']) < LOG_TIME):
#                     line = ser.readline().decode(errors='ignore').strip()
#                     if line:
#                         try:
#                             values = line.split(',')
#                             if len(values) == 5:
#                                 writer.writerow([datetime.now()] + values)
#                             else: print("mouse write error: csv has the wrong size")
#                         except ValueError as e:
#                             print(f"Error parsing line '{line}': {e}")
#                         except Exception as e:
#                             print(f"Unexpected error processing line '{line}': {e}")
#             finally:
#                 ser.close()
#                 print("Mouse logging finished")
#     except Exception as e:
#         print("Mouse log failure:", e)

def slip_data_pross(filename_slip, timing):
            df = pd.read_csv(filename_slip)
            df = df.fillna(0)
            start_arduino = pd.to_numeric(df['Time'].iloc[0])
            df["Time"] = timing['slip_start_log'] + pd.to_timedelta(df["Time"] - start_arduino, unit="us")
            df.to_csv(filename_slip, index=False)

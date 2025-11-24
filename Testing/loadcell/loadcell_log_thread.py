import time, serial, csv
import pandas as pd
import datetime
# time For simulating continuous data collection
from config import *


def log_load(timing, stop_event, filename, timing_lock, log_ready_event):
    try:
        print("enter_lc_logging")
        ser_lc = serial.Serial(ARDUINO_PORT['loadcell'], BAUD_RATE['loadcell'])
        for _ in range(10):
            ser_lc.readline()  # flush the buffer
        with timing_lock:
            timing['start_time_LC'] = time.time()

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Timestamp", "Shear_Force","Normal_Force"])
            log_ready_event.set()
            print(f"Loadcell Logging started for {LOG_TIME}s")
            try:
                while (not stop_event.is_set()) and ((time.time() - timing['start_time_LC']) < LOG_TIME):
                    line = ser_lc.readline().decode(errors='ignore').strip()
                    if line:
                        if not line.startswith("Force1(g),Force2(g)") and not line.startswith("Initializing") and not line.startswith("Load Cell") and not line.startswith("Taring") and not line.startswith("Offsets"):
                            try:
                                values = line.split(',')
                                if len(values) == 2:
                                    writer.writerow([datetime.now()] + values)
                                else: print("Loadcell write error: csv has the wrong size")
                            except ValueError as e:
                                print(f"Error parsing line '{line}': {e}")
                            except Exception as e:
                                print(f"Unexpected error processing line '{line}': {e}")
            finally:
                ser_lc.close()
                print("Loadcell logging finished")
    except Exception as e:
        print("Loadcell log failure:", e)


def load_data_pross(filename):
            df = pd.read_csv(filename)
            df = df.fillna(0)
            df.to_csv(filename, index=False)
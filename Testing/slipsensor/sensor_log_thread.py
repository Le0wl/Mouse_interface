import csv, time, serial
from datetime import datetime
from Testing.FCT_Arduino_interface.config import *

# data logging thread 
def log_data(stop_event, log_ready_event, filename, timing, timing_lock):
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
        for _ in range(10):
            ser.readline()  # flush the buffer
        with timing_lock:
            timing['start_time'] = time.time()

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Timestamp','Time', 'contact', 'delta_X', 'delta_Y','Movement'])
            print(f"Mouse Logging started for {LOG_TIME}s")
            log_ready_event.set()
            with timing_lock:
                timing['start_log'] = datetime.now()
            try:
                while (not stop_event.is_set()) and ((time.time() - timing['start_time']) < LOG_TIME):
                    line = ser.readline().decode(errors='ignore').strip()
                    if line:
                        values = line.split(',')
                        if len(values) == 5:
                            writer.writerow([datetime.now()] + values)
                        else: print("mouse write error: csv has the wrong size")
            finally:
                ser.close()
                print("Logging stopped")
    except Exception as e:
        print("mouse log failure:", e)


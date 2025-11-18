import sys
import os
import time
import rtde_control
import rtde_receive
import serial.tools.list_ports
import serial
import numpy as np
import csv
import threading
import datetime
import time # For simulating continuous data collection
# import csv, time, serial
# from datetime import datetime
from config import *


# --- Configuration ---
CSV_FILENAME = "sensor_data_log.csv"

HEADER = ["Timestamp","Relative_Time", 
          "Shear_Force","Normal_Force","Hook_Force","FSR_Reading",
          "Arm_Pos_X","Arm_Pos_Y","Arm_Pos_Z"
          ]


   # load_log_thread = threading.Thread(target= log_load, args=(timing, stop_event, filename_load))


def log_load(timing, stop_event, filename, timing_lock, log_ready_event):
    try:
        print("enter_lc_logging")
        ser_lc = serial.Serial(LC_ARDUINO_PORT, LC_BAUD_RATE)
        for _ in range(10):
            ser_lc.readline()  # flush the buffer
        with timing_lock:
            timing['start_time_LC'] = time.time()

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Timestamp", "Shear_Force","Normal_Force","Hook_Force"])
            log_ready_event.set()
            print(f"Loadcell Logging started for {LOG_TIME}s")
            try:
                while (not stop_event.is_set()) and ((time.time() - timing['start_time_LC']) < LOG_TIME):
                    line = ser_lc.readline().decode(errors='ignore').strip()
                    if line:
                        if not line.startswith("Force1(g),Force2(g),Force3(g),FSR(raw)") and not line.startswith("Initializing") and not line.startswith("Load Cell") and not line.startswith("Taring") and not line.startswith("Offsets"):
                            try:
                                values = line.split(',')
                                if len(values) == 3:
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




# --- Your data retrieval function (as defined above) ---
def log_data(rtde_r, ser):
    """
    Simulates getting some data.
    Returns a dictionary or a list of values for a single row.
    """
    global SCRIPT_START_TIME

    Shear_force = 0.0
    Normal_force = 0.0
    Hook_force = 0.0
    FSR_Reading = 0.0

    # Ensure SCRIPT_START_TIME is set. This handles cases where get_your_data might be called
    # before the main loop or if you call it directly for a single point.
    if SCRIPT_START_TIME is None:
        SCRIPT_START_TIME = time.time()

    # Calculate time elapsed since the script started
    relative_time_seconds = round(time.time() - SCRIPT_START_TIME, 2)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    arm_pos = rtde_r.getActualTCPPose() #record the initial pose of the robot

    if ser.in_waiting > 0:
        print("serial data available")
        try:
            line = ser.readline().decode('utf-8').strip()
            if line: # Ensure line is not empty
                 # Ignore potential header sent by Arduino on first boot
                if not line.startswith("Force1(g),Force2(g),Force3(g),FSR(raw)") and not line.startswith("Initializing") and not line.startswith("Load Cell") and not line.startswith("Taring") and not line.startswith("Offsets"):
                    # # Parse the CSV line from Arduino
                    try:
                        force1_str, force2_str, force3_str, FSR_str= line.split(',')
                        force1 = float(force1_str)
                        force2 = float(force2_str)
                        force3 = float(force3_str)
                        FSR_read = float(FSR_str)

                        # Round to 4 decimal places again, just to be safe with float precision
                        # This also handles potential rounding differences between Arduino and Python's float representation
                        Shear_force = round(force1, 2)
                        Normal_force = round(force2, 2)
                        Hook_force = round(force3, 2)
                        FSR_Reading = round(FSR_read, 2)

                    except ValueError as e:
                        print(f"Error parsing line '{line}': {e}")
                    except Exception as e:
                        print(f"Unexpected error processing line '{line}': {e}")
        except serial.SerialException as e:
            print(f"Serial communication error: {e}")
        except UnicodeDecodeError as e:
            print(f"UnicodeDecodeError: Could not decode byte: {e}. Skipping malformed line.")
    else:
        print("no serial data available!")
        
    # Small sleep to prevent busy-waiting, though ser.readline() blocks until data is available.
    # However, if data flow stops, we still want to check event_finished.
    # time.sleep(0.001)

    return {
        "Timestamp": timestamp,
        "Relative_Time": relative_time_seconds,
        "Shear_Force": Shear_force,
        "Normal_Force": Normal_force,
        "Hook_Force": Hook_force,
        "FSR_Reading": FSR_Reading,
        "Arm_Pos_X": round(arm_pos[0],4),
        "Arm_Pos_Y": round(arm_pos[1],4),
        "Arm_Pos_Z": round(arm_pos[2],4)
    }


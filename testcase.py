import serial
import csv
import time
import threading
import os
import io
from contextlib import redirect_stdout
from datetime import datetime
import pandas as pd
from armcontrol.ur_controller import UR
import numpy as np
from FCT_Arduino_interface.plotting import plot_hist

# --- Config ---
SERIAL_PORT = 'COM7'
BAUD_RATE = 500000
SAVE_PATH = 'logs'
LOG_TIME = 5
PLOT = True
UR_IP = '169.254.217.10'
MOVE = [0.02, 0, 0, 0, 0, 0]

# --- Data logging thread ---
def log_data(stop_event, filename, timing, timing_lock):
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
        for _ in range(10):
            ser.readline()  #flush the buffer
        with timing_lock:
            timing['start_time'] = time.time()

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Time', 'contact', 'delta_X', 'delta_Y'])
            print(f"Logging started for {LOG_TIME}s")
            try:
                while (not stop_event.is_set()) and ((time.time() - timing['start_time']) < LOG_TIME):
                    line = ser.readline().decode(errors='ignore').strip()
                    if line:
                        values = line.split(',')
                        if len(values) == 4:
                            writer.writerow(values)
                        else: print("write error: csv has the wrong size")
            finally:
                ser.close()
                print("Logging stopped")
    except Exception as e:
        print("log failure:", e)

# --- Robot motion thread ---
def move_robot(ur, timing, timing_lock):
    try:
        current_pose = ur.recv.getActualTCPPose()
        new_pos = np.array(current_pose) + np.array(MOVE)
        with timing_lock:
            timing['start_motion1'] = datetime.now()
        ur.move_pose_absolute(new_pos.tolist())
        with timing_lock:
            timing['end_motion1'] = datetime.now()
        time.sleep(2)
        with timing_lock:
            timing['start_motion2'] = datetime.now()
        ur.move_pose_absolute(current_pose)
        with timing_lock:
            timing['end_motion2'] = datetime.now()
        print("Robot motion done")
    except Exception as e:
        print("movement failure:",e)

# 1 for the forwards motion, -1 for the backwards motion, zero for no motion
def motion_timing(t, timing):
    if ('start_motion1'in timing) and ('end_motion2' in timing):
        if timing['start_motion1'] <= t <= timing['end_motion1']:
            return 1
        elif timing['start_motion2'] <= t <= timing['end_motion2']:
            return -1
        else:
            return 0
    else:
        return 0
    
    
def main():
    # --- Init ---
    thread_robo = True
    os.makedirs(SAVE_PATH, exist_ok=True)
    filename = os.path.join(SAVE_PATH, f"sensor_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv")
    ur = UR("UR5e", UR_IP)

    f = io.StringIO()
    with redirect_stdout(f):
        ur.connect()

    output = f.getvalue()
    if "cannot be connected" in output:
        thread_robo = False


    # --- Thread stuff ---
    timing = {}
    timing_lock = threading.Lock()
    stop_event = threading.Event()
    log_thread = threading.Thread(target=log_data, args=(stop_event, filename, timing, timing_lock))
    log_thread.start()

    if thread_robo:
        print('go_robo_thread')
        motion_thread = threading.Thread(target=move_robot, args=(ur, timing, timing_lock))
        motion_thread.start()

        motion_thread.join()
        stop_event.set()
    log_thread.join()

    # --- Process data ---
    if ('start_time'in timing):
        df = pd.read_csv(filename)
        df = df.fillna(0)
        start_arduino = pd.to_numeric(df['Time'].iloc[0])
        df["Time"] = datetime.fromtimestamp(timing['start_time']) + pd.to_timedelta(df["Time"] - start_arduino, unit="us")
        df["Motion"] = df['Time'].apply(lambda t: motion_timing(t, timing))
        df.to_csv(filename, index=False)
        print(f"Finished. File: {filename}")

        if PLOT:
            plot_hist(filename)
    else:
        print('no logging happened')


if __name__ == '__main__':
    main()
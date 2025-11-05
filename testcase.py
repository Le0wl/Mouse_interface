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

# Config 
SERIAL_PORT = 'COM7'
BAUD_RATE = 500000
SAVE_PATH = 'logs'
LOG_TIME = 30
PLOT = True
UR_IP = '169.254.123.10'
MOVE = [
    [0, -0.04, 0,  0, 0, 0], 
    [0, 0, 0.03,  0, 0, 0], 
    [0, 0, -0.03,  0, 0, 0],
    [0, 0.04, 0,  0, 0, 0],
    [0.02, 0, 0,  0, 0, 0], 
    [-0.02, 0, 0,  0, 0, 0]
    ]

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
            writer.writerow(['Time', 'contact', 'delta_X', 'delta_Y'])
            print(f"Mouse Logging started for {LOG_TIME}s")
            log_ready_event.set()
            with timing_lock:
                timing['start_log'] = datetime.now()
            try:
                while (not stop_event.is_set()) and ((time.time() - timing['start_time']) < LOG_TIME):
                    line = ser.readline().decode(errors='ignore').strip()
                    if line:
                        values = line.split(',')
                        if len(values) == 4:
                            writer.writerow(values)
                        else: print("mouse write error: csv has the wrong size")
            finally:
                ser.close()
                print("Logging stopped")
    except Exception as e:
        print("mouse log failure:", e)

# data logging thread
def log_robo(ur, filename2, stop_event, timing):
    try:
        with open(filename2, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Time', 'TCP_x', 'TCP_y', 'TCP_z', 'TCP_rot1', 'TCP_rot2', 'TCP_rot3'])
            print(f"Robot Logging started for {LOG_TIME}s")
            try:
                while (not stop_event.is_set()) and ((time.time() - timing['start_time']) < LOG_TIME):
                    time.sleep(0.01)
                    pose = ur.recv.getActualTCPPose()
                    if pose and len(pose) == 6:
                        writer.writerow([datetime.now()] + pose)
                    else:
                        print("upsi")
            finally:
                print("Robot Logging stopped")
    except Exception as e:
        print("robot log failure:", e)

# robot move thread 
def move_robot(ur, timing, timing_lock):
    try:
        print('go robo', MOVE)
        start_pose = ur.recv.getActualTCPPose()
        current_pose = start_pose
        for i, move in enumerate(MOVE):
            time.sleep(1)
            new_pos = np.array(current_pose) + np.array(move)
            with timing_lock:
                timing[f'start_motion{i}'] = datetime.now()
            ur.move_pose_absolute(new_pos.tolist())
            with timing_lock:
                timing[f'end_motion{i}'] = datetime.now()

            current_pose = ur.recv.getActualTCPPose()

        with timing_lock:
            timing[f'start_last_motion'] = datetime.now()
        ur.move_pose_absolute(start_pose)
        with timing_lock:
            timing[f'end_last_motion'] = datetime.now()

        print("Robot motion done")
    except Exception as e:
        print("movement failure:",e)

# 1 for the forwards motion, -1 for the backwards motion, zero for no motion
def motion_timing(t, timing, axis):
    axis_idx = {'x': 0, 'y': 1, 'z': 2}
    index = axis_idx[axis]

    if ('end_last_motion' in timing):
        for i, move in enumerate(MOVE):
            if timing[f'start_motion{i}'] <= t <= timing[f'end_motion{i}']:
                return move[index]
            
        if timing['start_last_motion'] <= t <= timing['end_last_motion']:
            return 0.01 # just spike in case of correction in whatever direction
    else:
        print('ERROR: Motion didnt finish')
    return 0
    
    
def main():
    # initiation of all the things
    thread_robo = True
    os.makedirs(SAVE_PATH, exist_ok=True)
    filename = os.path.join(SAVE_PATH, f"sensor_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv")
    filename2 = os.path.join(SAVE_PATH, f"robot_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv")

    ur = UR("UR5e", UR_IP)
    # overly complicated way to detect connection failure, but it works ¯\_(ツ)_/¯  
    f = io.StringIO()
    with redirect_stdout(f):
        ur.connect()
    output = f.getvalue()
    if "cannot be connected" in output:
        thread_robo = False
    # thread stuff 
    timing = {}
    timing_lock = threading.Lock()
    stop_event = threading.Event()
    log_ready_event = threading.Event()
    log_thread = threading.Thread(target=log_data, args=(stop_event, log_ready_event, filename, timing, timing_lock))
    motion_thread = threading.Thread(target=move_robot, args=(ur, timing, timing_lock))
    robo_log_thread = threading.Thread(target=log_robo, args=(ur, filename2, stop_event, timing))
    
    # log go
    log_thread.start()
    log_ready_event.wait() # waiting for logging set up because it takes forever 

    if thread_robo:
        robo_log_thread.start()
        motion_thread.start()
        motion_thread.join()
        time.sleep(1)
        stop_event.set()
    robo_log_thread.join()
    log_thread.join()
    # prettyfy data 
    if ('start_time'in timing):
        df = pd.read_csv(filename)
        df = df.fillna(0)
        start_arduino = pd.to_numeric(df['Time'].iloc[0])
        df["Time"] = timing['start_log'] + pd.to_timedelta(df["Time"] - start_arduino, unit="us")
        # df["Motion_x"] = df['Time'].apply(lambda t: motion_timing(t, timing, 'x'))
        # df["Motion_y"] = df['Time'].apply(lambda t: motion_timing(t, timing, 'y'))
        # df["Motion_z"] = df['Time'].apply(lambda t: motion_timing(t, timing, 'z'))
        df.to_csv(filename, index=False)
        print(f"Finished. File: {filename}")
    if ('start_time'in timing):
        df = pd.read_csv(filename2)
        df = df.fillna(0)
        start_x = pd.to_numeric(df['TCP_x'].iloc[0])
        start_y = pd.to_numeric(df['TCP_y'].iloc[0])
        start_z = pd.to_numeric(df['TCP_z'].iloc[0])
        df["TCP_x"] = pd.to_numeric(df['TCP_x']) - start_x
        df["TCP_y"] = pd.to_numeric(df['TCP_y']) - start_y
        df["TCP_z"] = pd.to_numeric(df['TCP_z']) - start_z
        df.to_csv(filename2, index=False)
        print(f"Finished. File: {filename2}")

        if PLOT:
            plot_hist(filename, filename2)
            
    else:
        print('no logging happened')

if __name__ == '__main__':
    main()
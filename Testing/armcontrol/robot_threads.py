import csv, time, io
from contextlib import redirect_stdout
import numpy as np
import pandas as pd
from datetime import datetime
from config import *
from armcontrol.ur_controller import UR



# data logging thread
def log_robo(ur, filename2, stop_event, timing):
    try:
        with open(filename2, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Time', 'TCP_x', 'TCP_y', 'TCP_z'])
            print(f"Robot Logging started for {LOG_TIME}s")
            try:
                while (not stop_event.is_set()) and ((time.time() - timing['start_time']) < LOG_TIME):
                    time.sleep(0.01)
                    pose = ur.recv.getActualTCPPose()
                    if pose and len(pose) == 6:
                        writer.writerow([datetime.now()] + pose[0,2])
                    else:
                        print(f"Robot log error: revieced unexpected data: {pose}")
            finally:
                print("Robot Logging stopped")
    except Exception as e:
        print("robot log failure:", e)


# robot move thread 
def move_robot(ur, timing, timing_lock):
    try:
        print('Motion:', MOVE)
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

        print("Robot motion thread finished")
    except Exception as e:
        print("Motion thread failure:",e)

def init_robot():
    thread_robo = False
    ur = UR("UR5e", UR_IP)
    # overly complicated way to detect connection failure, but it works ¯\_(ツ)_/¯  
    if(CONNECTIONS['robot']):
        f = io.StringIO()
        with redirect_stdout(f):
            ur.connect()
        output = f.getvalue()
        if "cannot be connected" in output:
            print(f"ERROR: cannot connect to: {UR_IP}, verify connection and IP")
        else:
            thread_robo = True
    return ur, thread_robo

def robot_data_pross(filename):
    df = pd.read_csv(filename)
    df = df.fillna(0)
    start_x = pd.to_numeric(df['TCP_x'].iloc[0])
    start_y = pd.to_numeric(df['TCP_y'].iloc[0])
    start_z = pd.to_numeric(df['TCP_z'].iloc[0])
    df["TCP_x"] = pd.to_numeric(df['TCP_x']) - start_x
    df["TCP_y"] = pd.to_numeric(df['TCP_y']) - start_y
    df["TCP_z"] = pd.to_numeric(df['TCP_z']) - start_z
    df.to_csv(filename, index=False)

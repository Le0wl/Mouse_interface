import csv, time
import numpy as np
from datetime import datetime
from Testing.FCT_Arduino_interface.config import *


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

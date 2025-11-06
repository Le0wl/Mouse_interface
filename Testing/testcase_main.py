import time, threading, os, io
from contextlib import redirect_stdout
from datetime import datetime
import pandas as pd
from armcontrol.ur_controller import UR
from armcontrol.robot_threads import *
from FCT_Arduino_interface.plotting import plot_hist
from FCT_Arduino_interface.sensor_log_thread import *
from config import *


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
        print(f"Finished mouse log. File: {filename}")
    else:
        print('no logging happened')
    if ('start_time'in timing) and thread_robo:
        df = pd.read_csv(filename2)
        df = df.fillna(0)
        start_x = pd.to_numeric(df['TCP_x'].iloc[0])
        start_y = pd.to_numeric(df['TCP_y'].iloc[0])
        start_z = pd.to_numeric(df['TCP_z'].iloc[0])
        df["TCP_x"] = pd.to_numeric(df['TCP_x']) - start_x
        df["TCP_y"] = pd.to_numeric(df['TCP_y']) - start_y
        df["TCP_z"] = pd.to_numeric(df['TCP_z']) - start_z
        df.to_csv(filename2, index=False)
        print(f"Finished robot log. File: {filename2}")

        if PLOT and os.path.exists(filename) and os.path.exists(filename2):
            plot_hist(filename, filename2)
            

if __name__ == '__main__':
    main()
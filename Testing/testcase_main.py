import time, threading, os, io
from contextlib import redirect_stdout
import datetime
import pandas as pd
from armcontrol.ur_controller import UR
from armcontrol.robot_threads import *
from plot.plotting import *
from slipsensor.sensor_log_thread import *
from loadcell.loadcell_log_thread import * 
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
    d = datetime.datetime
    thread_robo = True
    os.makedirs(SAVE_PATH, exist_ok=True)
    filename_slip = os.path.join(SAVE_PATH, f"sensor_log_{d.now().strftime('%Y-%m-%d_%H-%M-%S')}{SURFACE}.csv")
    filename_load = os.path.join(SAVE_PATH, f"load_log_{d.now().strftime('%Y-%m-%d_%H-%M-%S')}{SURFACE}.csv")
    filename_robo = os.path.join(SAVE_PATH, f"robot_log_{d.now().strftime('%Y-%m-%d_%H-%M-%S')}{SURFACE}.csv")

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
    slip_log_ready_event = threading.Event()
    load_log_ready_event = threading.Event()
    slip_log_thread = threading.Thread(target=log_slip, args=(stop_event, slip_log_ready_event, filename_slip, timing, timing_lock))
    motion_thread = threading.Thread(target=move_robot, args=(ur, timing, timing_lock))
    robo_log_thread = threading.Thread(target=log_robo, args=(ur, filename_robo, stop_event, timing))
    load_log_thread = threading.Thread(target= log_load, args=(timing, stop_event, filename_load, timing_lock, load_log_ready_event))
    
    # log go
    slip_log_thread.tstart()
    load_log_thread.start()
    if(slip_log_ready_event.wait(timeout=10) and load_log_ready_event.wait(timeout=10)): # waiting for logging set up /timeout at 10 secs 
        if thread_robo: # only start robo thread if the robot is connected
            robo_log_thread.start()
            motion_thread.start()
            motion_thread.join()
            time.sleep(1)
            stop_event.set() # stop the logging one second after the robot is done moving
            robo_log_thread.join()

        load_log_thread.join()
        slip_log_thread.join() 

        # prettyfy data 
        if ('start_time'in timing):
            df = pd.read_csv(filename_slip)
            df = df.fillna(0)
            start_arduino = pd.to_numeric(df['Time'].iloc[0])
            df["Time"] = timing['start_log'] + pd.to_timedelta(df["Time"] - start_arduino, unit="us")
            df.to_csv(filename_slip, index=False)
            print(f"Finished mouse log. File: {filename_slip}")
        else:
            print('no logging happened')

        if ('start_time'in timing) and thread_robo:
            df = pd.read_csv(filename_robo)
            df = df.fillna(0)
            start_x = pd.to_numeric(df['TCP_x'].iloc[0])
            start_y = pd.to_numeric(df['TCP_y'].iloc[0])
            start_z = pd.to_numeric(df['TCP_z'].iloc[0])
            df["TCP_x"] = pd.to_numeric(df['TCP_x']) - start_x
            df["TCP_y"] = pd.to_numeric(df['TCP_y']) - start_y
            df["TCP_z"] = pd.to_numeric(df['TCP_z']) - start_z
            df.to_csv(filename_robo, index=False)
            print(f"Finished robot log. File: {filename_robo}")

            if PLOT and os.path.exists(filename_slip) and os.path.exists(filename_robo):
                plot_hist_sensor_robot(filename_slip, filename_robo)


    else: 
        print("ERROR: Logging setup did not complete within 10 seconds. Terminating.")
        stop_event.set()
        return 0
            

if __name__ == '__main__':
    main()
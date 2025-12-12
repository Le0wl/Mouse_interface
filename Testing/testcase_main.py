import time, threading, os
from datetime import datetime
from armcontrol.ur_controller import UR
from armcontrol.robot_threads import *
from plot.plotting import *
from slipsensor.sensor_log_thread import *
from loadcell.loadcell_log_thread import * 
from config import *
from vision.capture import *
from vision.marker_detection import *
from sklearn.linear_model import RANSACRegressor, LinearRegression


def serial_logger(name, filename, log_ready_event, timing, timing_lock, stop_event):
    try:
        dt = datetime.datetime
        ser = serial.Serial(ARDUINO_PORT[name], BAUD_RATE[name])
        ser.reset_input_buffer()

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(COLUMNS[name])
            print(f"{name} Logging started for {LOG_TIME}s")
            log_ready_event.set()
            t0 = dt.now()
            start_time = t0
            with timing_lock:
                timing[f'{name}_start_log'] = t0
            try:
                while (not stop_event.is_set()) and ((dt.now() - start_time).total_seconds() < LOG_TIME):
                    line = ser.readline().decode(errors='ignore').strip()
                    if line:
                        if not line.startswith("Force1(g),Force2(g)") and not line.startswith("Initializing") and not line.startswith("Load Cell") and not line.startswith("Taring") and not line.startswith("Offsets"):
                            try:
                                values = line.split(',')
                                if len(values) == len(COLUMNS[name])-1:
                                    writer.writerow([dt.now()] + values)
                                else: print(f"{name} write error: csv has the wrong size:{values}")
                            except ValueError as e:
                                print(f"{name}: Error parsing line '{line}': {e}")
                            except Exception as e:
                                print(f"{name}: Unexpected error processing line '{line}': {e}")
            finally:
                time.sleep(1)
                ser.close()
                print(f"{name} logging finished")
    except Exception as e:
        print(f"{name} log failure:", e)

        
def main_thread():
    # initiation of all the things
    start_time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    os.makedirs(SAVE_PATH, exist_ok=True)
    filename_slip = os.path.join(SAVE_PATH, f"slip/slip_log_{start_time_str}{SURFACE}.csv")
    filename_load = os.path.join(SAVE_PATH, f"loadcell/load_log_{start_time_str}{SURFACE}.csv")
    filename_robo = os.path.join(SAVE_PATH, f"robot/robot_log_{start_time_str}{SURFACE}.csv")
    ur, thread_robo = init_robot()
    
    # thread stuff 
    timing = {}
    timing_lock = threading.Lock()
    stop_event = threading.Event()
    slip_log_ready_event = threading.Event()
    load_log_ready_event = threading.Event()
    camera_ready_event = threading.Event()
    video_file = [None]

    slip_log_thread = threading.Thread(target=serial_logger, args=('slip', filename_slip, slip_log_ready_event, timing, timing_lock, stop_event))
    load_log_thread = threading.Thread(target=serial_logger, args=('loadcell', filename_load, load_log_ready_event, timing, timing_lock, stop_event))
    motion_thread = threading.Thread(target=move_robot, args=(ur, timing, timing_lock))
    robo_log_thread = threading.Thread(target=log_robo, args=(ur, filename_robo, stop_event, timing))
    camera_thread = threading.Thread(target = film_thread, args=(camera_ready_event,stop_event,  video_file))

    # log go
    ready = []
    if (CONNECTIONS['slip']):
        slip_log_thread.start()
        ready.append(slip_log_ready_event)

    if (CONNECTIONS['loadcell']):
        load_log_thread.start()
        ready.append(load_log_ready_event)

    if (CONNECTIONS['camera']):
        camera_thread.start()
        ready.append(camera_ready_event)

    if(all(evt.wait(timeout=10) for evt in ready)): # waiting for logging set up /timeout at 10 secs 
        if thread_robo and (CONNECTIONS['slip']): # only start robo thread if the robot is connected
            robo_log_thread.start()
            motion_thread.start()
            motion_thread.join()
            time.sleep(1)
            stop_event.set() # stop the logging one second after the robot is done moving
            robo_log_thread.join()

        if (CONNECTIONS['loadcell']):
            load_log_thread.join()
        if (CONNECTIONS['slip']):
            slip_log_thread.join() 
        if (CONNECTIONS['camera']):
            camera_thread.join() 
    
        # prettyfy data 
        if ('slip_start_log'in timing):
            sync_arduino_clock(filename_slip)
            print(f"Finished mouse log. File: {filename_slip}")
        else:
            print('no slip logging happened')

        if thread_robo:
            robot_data_pross(filename_robo)
            print(f"Finished robot log. File: {filename_robo}") 
        else:
            print('no robot logging happened')

        if ('loadcell_start_log'in timing):
            sync_arduino_clock(filename_load)
            print(f"Finished load log. File: {filename_load}")
        else:
            print('no load logging happened')

        if (CONNECTIONS['camera']):
            files = marker_logging(video_file[0])
            print('marker logging finished')

    else: 
        print("ERROR: Logging setup did not complete within 10 seconds. Terminating.")
        stop_event.set()
    return start_time_str

# def slip_data_pross(filename_slip, timing):
#             df = pd.read_csv(filename_slip)
#             df = df.fillna(0)
#             df['Timestamp']= pd.to_datetime(df['Timestamp'])
#             df['Arduino_Time'] = pd.to_numeric(df['Arduino_Time'])
#             timestamps = df['Timestamp'].unique()
#             if len(df.loc[df['Timestamp']==timestamps[0]])<3:       # clear incomplete package 
#                 df.drop(df.loc[df['Timestamp']==timestamps[0]].index, inplace=True)
#                 timestamps = df['Timestamp'].unique()
#             first_package_size = len(df.loc[df['Timestamp']==timestamps[0]])
#             df = df.iloc[first_package_size-1:]                    # keep the last value from the first timestamp and the rest
#             start_arduino = df['Arduino_Time'].iloc[0]
#             start_log = df['Timestamp'].iloc[0]
#             synch_time = [start_log]
#             for t in range(len(timestamps)-1):
#                 package = df.loc[df['Timestamp']==timestamps[t]]
#                 end_arduino = package['Arduino_Time'].iloc[-1]
#                 delta_log = timestamps[t] -start_log
#                 delta_arduino =  pd.to_timedelta(end_arduino - start_arduino, unit="us")
#                 if (delta_log -delta_arduino)< pd.to_timedelta(1, unit="ms") and (delta_log -delta_arduino) >0:
#                     synch_time.append(start_log + pd.to_timedelta(package["Arduino_Time"].iloc[:-1] - start_arduino, unit="us"))
#                     synch_time.append(timestamps[t]) # realign to the master clock to prevent drift
#                 else:
#                     ta = package["Arduino_Time"].iloc[:-1] * delta_log/delta_arduino  # stretch time
#                     synch_time.append(start_log + pd.to_timedelta(ta - start_arduino, unit="us"))
#                     synch_time.append(timestamps[t])  # realign to the master clock to prevent drift
#                 start_log = timestamps[t]
#                 start_arduino = end_arduino

#             df["Time"] = synch_time

#             df.to_csv(filename_slip+"2", index=False)


def sync_arduino_clock(filename):
    df = pd.read_csv(filename)
    df = df.fillna(0)

    # convert master timestamps to datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df["Arduino_Time"] = pd.to_numeric(df["Arduino_Time"])

    # detect if first package is cut off (< 3 samples)
    if len(df[df['Timestamp']==df['Timestamp'].iloc[0]])<3:
        df = df[df['Timestamp']!=df['Timestamp'].iloc[0]]

    # identify one reference Arduino timestamp per packet (last sample)
    packet_last = df.groupby('Timestamp')["Arduino_Time"].last().reset_index()

    # convert for fitting
    T_master = packet_last['Timestamp'].astype('int64') * 1e-9     # seconds
    T_arduino = packet_last["Arduino_Time"] * 1e-6                 # seconds

    X = T_arduino.values.reshape(-1, 1)
    y = T_master.values

    # robust fit: eliminates latency spikes automatically
    ransac = RANSACRegressor(
        estimator=LinearRegression(),
        residual_threshold=0.005,   # 5 ms tolerance for latency jitter
        max_trials=1000,
        random_state=0
    )
    ransac.fit(X, y)

    b = ransac.estimator_.coef_[0]
    a = ransac.estimator_.intercept_

    # apply mapping to EVERY sample
    df["Sync_Time"] = a + b * (df["Arduino_Time"] * 1e-6)   # seconds
    df["Sync_Time"] = pd.to_datetime(df["Sync_Time"], unit='s')
    df["Simple_Time"] = df["Timestamp"].iloc[0] +pd.to_timedelta(df["Arduino_Time"], unit="us")

    df.to_csv(filename, index=False)

    return 


if __name__ == '__main__':
    test_detection()
    start_time = main_thread()
    run, markers = get_all_paths(f"logs/slip/slip_log_{start_time}{SURFACE}.csv")
    plot_vid_slip(run.slip, markers.m1, markers.m2, markers.m3, markers.m4, markers.time)

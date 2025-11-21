import time, threading, os
from datetime import datetime as dt
from armcontrol.ur_controller import UR
from armcontrol.robot_threads import *
from plot.plotting import *
from slipsensor.sensor_log_thread import *
from loadcell.loadcell_log_thread import * 
from config import *

def serial_logger(name, filename, log_ready_event, timing, timing_lock, stop_event):
    try:
        ser = serial.Serial(ARDUINO_PORT[name], BAUD_RATE[name])
        for _ in range(10):
            ser.readline()  # flush the buffer
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(COLUMNS[name])
            print(f"{name} Logging started for {LOG_TIME}s")
            log_ready_event.set()
            start_time = time.time()
            with timing_lock:
                timing[f'{name}_start_log'] = dt.now()
            try:
                while (not stop_event.is_set()) and ((time.time() - start_time) < LOG_TIME):
                    line = ser.readline().decode(errors='ignore').strip()
                    if line:
                        if not line.startswith("Force1(g),Force2(g)") and not line.startswith("Initializing") and not line.startswith("Load Cell") and not line.startswith("Taring") and not line.startswith("Offsets"):
                            try:
                                values = line.split(',')
                                if len(values) == len(COLUMNS[name])-1:
                                    writer.writerow([dt.now()] + values)
                                else: print(f"{name} write error: csv has the wrong size")
                            except ValueError as e:
                                print(f"{name}: Error parsing line '{line}': {e}")
                            except Exception as e:
                                print(f"{name}: Unexpected error processing line '{line}': {e}")
            finally:
                ser.close()
                print(f"{name} logging finished")
    except Exception as e:
        print(f"{name} log failure:", e)

        
def main():
    # initiation of all the things
    os.makedirs(SAVE_PATH, exist_ok=True)
    filename_slip = os.path.join(SAVE_PATH, f"slip_log_{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}{SURFACE}.csv")
    filename_load = os.path.join(SAVE_PATH, f"load_log_{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}{SURFACE}.csv")
    filename_robo = os.path.join(SAVE_PATH, f"robot_log_{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}{SURFACE}.csv")
    ur, thread_robo = init_robot()
    
    # thread stuff 
    timing = {}
    timing_lock = threading.Lock()
    stop_event = threading.Event()
    slip_log_ready_event = threading.Event()
    load_log_ready_event = threading.Event()

    slip_log_thread = threading.Thread(target=serial_logger, args=('slip', filename_slip, slip_log_ready_event, timing, timing_lock, stop_event))
    load_log_thread = threading.Thread(target=serial_logger, args=('loadcell', filename_load, load_log_ready_event, timing, timing_lock, stop_event))
    motion_thread = threading.Thread(target=move_robot, args=(ur, timing, timing_lock))
    robo_log_thread = threading.Thread(target=log_robo, args=(ur, filename_robo, stop_event, timing))
    
    # log go
    ready = []
    if (CONNECTIONS['slip']):
        print('eyyo')
        slip_log_thread.start()
        ready.append(slip_log_ready_event)

    if (CONNECTIONS['loadcell']):
        load_log_thread.start()
        ready.append(load_log_ready_event)

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

        to_plot = []
        # prettyfy data 
        if ('slip_start_log'in timing):
            slip_data_pross(filename_slip, timing)
            print(f"Finished mouse log. File: {filename_slip}")
            to_plot.append(filename_slip)
        else:
            print('no slip logging happened')

        if thread_robo:
            robot_data_pross(filename_robo)
            print(f"Finished robot log. File: {filename_robo}") 
            to_plot.append(filename_robo)       
        else:
            print('no robot logging happened')

        if ('loadcell_start_log'in timing):
            load_data_pross(filename_load)
            print(f"Finished load log. File: {filename_load}")
            to_plot.append(filename_load)
        else:
            print('no load logging happened')

        if PLOT:
            plot_hist_sensors_robot(*to_plot)
    else: 
        print("ERROR: Logging setup did not complete within 10 seconds. Terminating.")
        stop_event.set()

if __name__ == '__main__':
    main()

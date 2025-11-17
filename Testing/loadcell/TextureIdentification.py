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

# Get the directory of the current script (e.g., /path/to/my_project/tests)
current_script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory of the current script's directory
# This moves you from '/path/to/my_project/tests' to '/path/to/my_project'
project_root_dir = os.path.join(current_script_dir, '..')
# Normalize the path to remove any '..' or '.'
project_root_dir = os.path.normpath(project_root_dir)
# Add the project root directory to sys.path
# Use insert(0, ...) to prioritize this path
if project_root_dir not in sys.path:
    sys.path.insert(0, project_root_dir)

#from Library.dynamixel_controller import Dynamixel
#from Library.MelexIO import MelexIO

# --- Configuration ---
CSV_FILENAME = "sensor_data_log.csv"

HEADER = ["Timestamp","Relative_Time", 
          "Shear_Force","Normal_Force","Hook_Force","FSR_Reading",
          "Arm_Pos_X","Arm_Pos_Y","Arm_Pos_Z"
          ]


# Set the correct COM port for your Arduino.
LC_ARDUINO_PORT = 'COM8'
LC_BAUD_RATE = 115200

# --- Global variable to store the script start time ---
# This will be set once when the script begins execution
SCRIPT_START_TIME = None
record_frequency_seconds=0.1

# --- Shared resources and synchronization primitives ---
# Event to signal when Thread A has finished
motion_finished = threading.Event()

global CYCLE_COUNT

CYCLE_COUNT = 5

# --- Your data retrieval function (as defined above) ---
def get_data(rtde_r, ser):
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


# --- Data Collection and Writing ---
def record_data_to_csv(data_point, filename=CSV_FILENAME, header=HEADER):
    """
    Records a single data point to a CSV file.
    If the file doesn't exist, it creates it and writes the header.
    Otherwise, it appends the data without writing the header again.
    """
    file_exists = os.path.isfile(filename)

    # 'a' mode opens the file for appending. If it doesn't exist, it creates it.
    # newline='' is crucial to prevent extra blank rows in CSV
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)

        if not file_exists:
            writer.writeheader() # Write header only if file is new

        writer.writerow(data_point) # Write the data row


def motion_thread_function(rtde_r,rtde_c):
    print("Motion Thread: Starting execution...")

    start_TCP_Pose = rtde_r.getActualTCPPose() #record the initial pose of the robot
    end_TCP_Pose = start_TCP_Pose.copy()
    #end_TCP_Pose[0] = start_TCP_Pose[0] + 0.05 #make the tool move left 0.05m
    #end_TCP_Pose[1] = start_TCP_Pose[1] + 0.05 #make the tool move back 0.05m
    #end_TCP_Pose[2] = start_TCP_Pose[2] + 0.05 #make the tool move up 0.05m
    #print(start_TCP_Pose)
    #print(end_TCP_Pose)
    global CYCLE_COUNT
    try:
        # record data at certain interval
        for i in range(0, CYCLE_COUNT, 1): # move CYCLECOUNT times
            end_TCP_Pose[2] = start_TCP_Pose[2] + 0.05 #make the tool move up 0.05m
            rtde_c.moveL(end_TCP_Pose, 0.1, 0.1)#go up and extend finger
            time.sleep(5)
            end_TCP_Pose[1] = start_TCP_Pose[1] - 0.07 
            rtde_c.moveL(end_TCP_Pose, 0.1, 0.1)#make the tool move forward 0.07m
            #time.sleep(0.5)
            end_TCP_Pose[2] = start_TCP_Pose[2]
            rtde_c.moveL(end_TCP_Pose, 0.1, 0.1) #move back down 0.05m
            time.sleep(5)
            end_TCP_Pose[1] = start_TCP_Pose[1]
            rtde_c.moveL(end_TCP_Pose, 0.1, 0.02)#make the tool move back 0.07m /was 0.2 for early experiments
            time.sleep(3)
           
            #time.sleep(0.5)
    finally:
        # Signal that Motion Thread has finished, regardless of how it exits
        print("Motion Thread: Signalling that I have finished.")
        time.sleep(5)
        motion_finished.set() # Set the event to true
        print("Motion Thread: Exiting.")

# --- Thread B: The data recording thread ---
def recording_thread_function(rtde_r, ser):
    print("Recording Thread: Waiting for Motion Thread to start...")

    # Wait for Thread A to start (optional, but ensures A is running)
    # In this setup, we actually start B immediately after A,
    # and B just starts recording. The main loop ensures it doesn't
    # start before A unless A takes longer to initialize.
    # We could add a separate event for "Thread A started" if needed.

    print(f"Recording Thread: Starting data recording at {record_frequency_seconds} second intervals...")
    print(f"Recording Thread: Starting data logging to {CSV_FILENAME}...")
    print("Press Ctrl+C to stop.")


    record_count = 0
    while not motion_finished.is_set(): # Keep recording as long as Thread A is not finished
        try:
            #recording data
            data = get_data(rtde_r,ser)
            record_data_to_csv(data)
            record_count += 1

            # Sleep for the set frequency, but wake up early if A finishes
            motion_finished.wait(record_frequency_seconds)

        except Exception as e:
            print(f"Recording Thread: An error occurred during recording: {e}")
            break # Exit loop on error

    print("Recording Thread: Motion Thread has finished. Stopping data recording.")
    print(f"Recording Thread: Total data points recorded: {record_count}")
    print("Logging finished.")
    print("Recording Thread: Exiting.")

#main function, mostly just organizing threads
def main():
    print("Main: Starting main execution...")
    #create shared handles
    #UR5e setup
    rtde_r = rtde_receive.RTDEReceiveInterface("192.168.56.101")
    rtde_c = rtde_control.RTDEControlInterface("192.168.56.101")
    #setup Serial for arduino
    ser = serial.Serial(LC_ARDUINO_PORT, LC_BAUD_RATE, timeout=1) # timeout helps prevent infinite blocking
    time.sleep(2) # Give serial connection time to establish

    # Create the threads
    Motion_thread = threading.Thread(target=motion_thread_function, name="Motion_Thread", args=(rtde_r,rtde_c))
    Recording_thread = threading.Thread(target=recording_thread_function, name="Recording_Thread", args=(rtde_r, ser)) # Record every 0.1 seconds
   
    # Start Thread A
    print("Main: Starting Motion Thread...")
    Motion_thread.start()

    # Start Thread B immediately after Thread A (or as close as possible)
    print("Main: Starting Recording Thread...")
    Recording_thread.start()

    # Wait for Thread A to complete.
    # This is important if you want the main script to wait for A.
    # Thread B is already waiting for A to finish via the 'thread_a_finished' event.
    print("Main: Waiting for Motion Thread to join...")
    Motion_thread.join() # Blocks until thread_a completes

    # Now that Thread A has finished and set the event, Thread B should
    # naturally exit its loop and complete. We wait for it to join too.
    print("Main: Waiting for Recording Thread to join...")
    Recording_thread.join() # Blocks until thread_b completes

    #close all comms properlly
    time.sleep(0.1)

    ser.close()
    print("Serial port closed.")
    print("Main: All threads have finished. Exiting main program.")
    


if __name__ == '__main__': main()
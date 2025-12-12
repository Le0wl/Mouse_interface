import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from plot.utils import *
import re
import datetime

# full plotter of all the things
def plot_hist_sensors_robot(file_slip = None, file_robot = None, file_load = None):
    df_slip, df_load, df_robot = synch(file_slip, file_robot, file_load)  
    # df_slip, df_load, df_robot = preprocessing(file_slip, file_robot, file_load)  

    plt.figure(figsize=(12,4))
    if file_slip is not None:
        # plot_mvt(df_slip)
        plot_slip(df_slip)

    if file_robot is not None:
        # plot_robot(df_robot)

        plot_robot_speed(df_robot)
    if file_load is not None:
        plot_shear(df_load)
        # plot_shear(df_load, 'deriv')

    plt.xlabel('Time (s)')
    plt.ylabel('Sensor Values')
    plt.grid(True)
    plt.legend()
    plt.savefig("figs/test_hist_sensors_robot.png")
    plt.show()
        
def subplot_hist_sensors_robot(ax, file_slip = None, file_robot = None, file_load = None):
    df_slip, df_load, df_robot = synch(file_slip, file_robot, file_load)   
    if file_slip is not None:
        try:
            ax.plot(df_slip['Time_rel'],df_slip['contact'], label = 'contact', color = 'g')
            ax.plot(df_slip['Time_rel'], df_slip['delta_X'], label='delta_X', color = 'teal')
            ax.plot(df_slip['Time_rel'], df_slip['delta_Y'], label='delta_Y', color = 'blue')
        except Exception as e:
            print(f"ERROR slip plotting:", e)
    if file_load is not None:
        try:
            ax.plot(df_load['Time_rel'],df_load['Shear_Force'], label = 'LC Shear Force', color = 'orange')
            if "Normal_Force" in df_load.columns:
                ax.plot(df_load['Time_rel'],df_load['Normal_Force'], label = 'LC Normal Force', color = 'coral')
        except Exception as e:
            print(f"ERROR load plotting:", e)
    if file_robot is not None:
        try:
            ax.plot(df_robot['Time_rel'],df_robot['TCP_x']*100, label = 'arm pos in x[cm]', color = 'm')
            ax.plot(df_robot['Time_rel'],df_robot['TCP_y']*100, label = 'arm pos in y[cm]', color = 'pink')
            ax.plot(df_robot['Time_rel'],df_robot['TCP_z']*100, label = 'arm pos in z[cm]', color = 'purple')
        except Exception as e:
            print(f"ERROR robot plotting:", e)
    ax.set_ylim([-60,60])
    return ax


def plot_average(file_slip, file_robot, file_load):
    df_slip, df_load, df_robot = synch(file_slip, file_robot, file_load) 
    df_slip['contact'] = df_slip['contact'].apply(lambda x: 1 if x >contact_thresh else 0)
    df_slip = moving_averge(df_slip, 6)   
    df_slip['contact'] = df_slip['contact'].apply(lambda x: 0 if x < 1 else 1)
    plot_slip(df_slip)
    # plot_mvt(df_slip)
    plot_shear(df_load)
    plot_robot(df_robot)
    # plot_lc(df_load)
    plt.legend()
    # plt.grid()
    plt.show()


# plot histogram only sensor
def plot_hist_slip(file):
    df_log = pd.read_csv(file)
    df_log['Time'] = pd.to_datetime(df_log['Time'], format='%Y-%m-%d %H:%M:%S.%f')
    df_log['Time_rel'] = (df_log['Time'] - df_log['Time'].iloc[0]).dt.total_seconds()
    plt.figure(figsize=(8,4))
    plot_mvt(df_log)
    plt.xlabel('Time (s)')
    plt.ylabel('Delta Values')
    plt.title('x and y deltas over time')
    plt.grid(True)
    plt.legend()
    plt.savefig("figs/deltahist_sensor.png")
    plt.show()

def plot_load_ideas(file_lc, file_ro, file_sl):
    df_slip, df_load, df_robot = synch(file_load=file_lc, file_robot=file_ro, file_slip=file_sl) 
    df_load['deriv'] = shear_derivative(df_load)
    
    plot_shear(df_load)
    plot_robot_speed(df_robot)
    # plot_slip(df_slip=df_slip)
    plt.grid()
    plt.legend()
    plt.show()


# plot 2D path in mm
def plot_path(file):
    df_log = pd.read_csv(file)
    #conversion from dots to mm determined empirically not precise
    df_log['x'] = df_log['delta_X'].cumsum()/32 * -1 
    df_log['y'] = df_log['delta_Y'].cumsum()/32 * -1
    plt.figure(figsize=(6,6))
    plt.plot(df_log['x'], df_log['y'], color='green')
    plt.xlabel('X position mm')
    plt.ylabel('Y position mm')
    plt.title('2D Motion Path ')
    plt.axis('equal')  
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("figs/path_mm.png")
    plt.show()

# plot deltas in a 2d square to see if the saturate
def plot_xyDeltas(file):
    df_log = pd.read_csv(file)
    # plot deltas
    plt.figure(figsize=(6,6))
    plt.plot(df_log['delta_X'], df_log['delta_Y'], color='red')
    plt.xlabel('X position (pixels or counts)')
    plt.ylabel('Y position (pixels or counts)')
    plt.title('2D Motion Path from Sensor Deltas')
    plt.axis('equal')   
    plt.savefig("figs/deltapath.png")
    plt.show()


def plot_lc(df_load):
    plt.scatter(df_load['Time_rel'],df_load['Shear_Force']/1000*9.81 * 10, label = 'LC Shear Force [0.1 N]', color = 'orange', marker= '+')
    plt.scatter(df_load['Time_rel'],df_load['Normal_Force']/1000*9.81, label = 'LC Normal Force [1 N]', color = 'coral', marker= '+')

def plot_slip(df_slip):
    # plt.plot(df_slip['Time_rel'],df_slip['contact']*5, label = 'contact', color = 'lime')
    df_slip['contact'] = df_slip['contact'].apply(lambda x: 1 if x >contact_thresh else 0)
    plt.plot(df_slip['Sync_Time'],df_slip['contact']*5, label = 'contact', color = 'g')
    plt.plot(df_slip['Sync_Time'], df_slip['delta_X'], label='delta_X', color = 'teal')
    plt.plot(df_slip['Sync_Time'], df_slip['delta_Y'], label='delta_Y', color = 'lightblue')

def plot_robot(df_robot):
    plt.plot(df_robot['Time_rel'],df_robot['TCP_x']*100, label = 'arm pos in x [cm]', color = 'm')
    plt.plot(df_robot['Time_rel'],df_robot['TCP_y']*100, label = 'arm pos in y [cm]', color = 'pink')
    plt.plot(df_robot['Time_rel'],df_robot['TCP_z']*100, label = 'arm pos in z [cm]', color = 'purple')

def plot_robot_speed(df_robot):
    df_robot['d_x'], df_robot['d_y'], df_robot['d_z'] = arm_speed(df_robot)
    plt.plot(df_robot['Time_rel'],df_robot['d_x'], label = 'arm speed in x [cm/s]', color = 'm')
    plt.plot(df_robot['Time_rel'],df_robot['d_y'], label = 'arm speed in y [cm/s]', color = 'blue')
    plt.plot(df_robot['Time_rel'],df_robot['d_z'], label = 'arm speed in z [cm/s]', color = 'purple')

def compare(path_lists, title = "tracking on different surfaces"):
    mode = len(path_lists)
    tot = len(path_lists[0])
    fig, axs = plt.subplots(tot, mode, sharex=True, figsize=(7*mode,4*tot))
    if mode == 1: 
        path_list = path_lists[0]
        for i in range(tot):
            slip = path_list[i].slip
            rob = path_list[i].robo
            load = path_list[i].load
            subplot_hist_sensors_robot(file_slip=slip,file_robot=rob, file_load=load, ax=axs[i])
            m = re.search(r'_\d{2}-\d{2}-\d{2}', slip)
            if m:
                subtitle = slip[m.end():-4]
                axs[i].set_title(f"on {subtitle}")
        axs[0].legend(loc="upper right")
    else:
        for j in range(mode):
            path_list = path_lists[j]
            for i in range(tot):
                slip = path_list[i].slip
                rob = path_list[i].robo
                load = path_list[i].load
                subplot_hist_sensors_robot(file_slip=slip,file_robot=rob, file_load=load, ax=axs[i,j])
                m = re.search(r'_\d{2}-\d{2}-\d{2}', slip)
                if m:
                    subtitle = slip[m.end():-4]
                    axs[i,j].set_title(f"on {subtitle}")
        axs[0,j].legend(loc="upper right")
    fig.suptitle(title)
    fig.supxlabel('time [s]')
    fig.supylabel('sensor values')
    plt.subplots_adjust(wspace=0.1, hspace=0.4)
    fig.savefig("figs/test_sensor_robot_compare_test.png")
    plt.show()


def plot_markerpos(log1, log2, log3, log4):
    # df1, df2, df3, df4 = marker_data_pross(log1, log2, log3, log4)
    df = marker_panda(log1, log2, log3, log4)

    plt.scatter(df['Time_rel'],df['x0'], label = 'aruco marker1 in x', color = 'pink', marker='+')
    plt.scatter(df['Time_rel'],df['x1'], label = 'aruco marker2 in x', color = 'blue', marker='+')
    plt.scatter(df['Time_rel'],df['x2'], label = 'aruco marker3 in x', color = 'orange', marker='+')
    plt.scatter(df['Time_rel'],df['x3'], label = 'aruco marker4 in x', color = 'violet', marker='+')
    plt.legend()
    plt.show()
    plt.plot(df['Time_rel'],df['delta_x0'], label = 'speed marker1', color = 'pink')
    plt.plot(df['Time_rel'],df['delta_x1'], label = 'speed marker2', color = 'blue')
    plt.plot(df['Time_rel'],df['delta_x2'], label = 'speed marker3', color = 'orange')
    plt.legend()
    plt.show()

def marker_path(*files):
    plt.figure(figsize=(5,4))
    for file in files:
        df_marker = pd.read_csv(file)
        plt.scatter(df_marker['x'], -df_marker['y'], marker='+')
    plt.xlabel('X position mm')
    plt.ylabel('Y position mm')
    plt.title('2D Motion Path ')
    plt.grid(True)
    plt.xlim([0,640])
    plt.ylim([-360,0])
    plt.tight_layout()
    plt.savefig("figs/path_mm.png")
    plt.show()

def plot_mvt(df_slip):
    df_slip = slip_detection(df_slip)
    plt.plot(df_slip['Sync_Time'], df_slip['slip']*2, label='slip detected', color = 'red')
    plt.plot(df_slip['Sync_Time'], df_slip['mvt'], label='movement detected', color = 'g')

def plot_vid_slip(slip_path, m1_path,  m2_path,  m3_path,  m4_path, mtime_path):
    df_slip, df_marker= vid_synch(slip_path, m1_path,  m2_path,  m3_path,  m4_path, mtime_path) 
    plt.figure(figsize=(12,4))
    plot_marker(df_marker)
    plot_mvt(df_slip)
    plt.grid()
    plt.ylim(-10,10)
    plt.legend(loc="lower right")
    plt.show()

def plot_marker(df):
    plt.plot(df['Timestamp']+pd.to_timedelta(270, unit= "ms"),df['dx2']/10, label = 'marker sled horizonal pos [cm]', color = 'orange')
    plt.plot(df['Timestamp']+pd.to_timedelta(270, unit= "ms"),df['dy2']/10, label = 'marker sled vertical pos [cm]', color = 'cyan')
    plt.plot(df['Timestamp']+pd.to_timedelta(270, unit= "ms"),df['slip']*4, label = 'sled slip horizonal', color = 'blue')

def compare_slip_time(filename):
    df = pd.read_csv(filename)
    arduino = pd.to_numeric(df['Arduino_Time'])
    arduino = pd.to_timedelta(arduino - arduino[0], unit = "us")
    timestamp = pd.to_datetime(df['Timestamp'])
    timestamp_us = pd.to_timedelta(timestamp- timestamp[0], unit ="us")
    old_time = pd.to_datetime(df["Simple_Time"])
    old_time_us = pd.to_timedelta(old_time - timestamp[0], unit ="us")
    new_time = pd.to_datetime(df['Sync_Time'])
    new_time_us = pd.to_timedelta(new_time- timestamp[0], unit ="us")
    index = range(len(df))
    # plt.plot(index, old_time_us, label ="old" )
    # plt.plot(index, new_time_us, label = "new")
    # plt.plot(index, timestamp_us, label = "stamp")
    # plt.plot(index, arduino, label = "arduino")

    plt.scatter(index, old_time_us, label ="old", marker = '+')
    plt.scatter(index, new_time_us, label = "new", marker = '+')
    plt.scatter(index, timestamp_us, label = "stamp", marker = '+')
    plt.scatter(index, arduino, label = "arduino", marker = '+')

    plt.legend()
    plt.show()



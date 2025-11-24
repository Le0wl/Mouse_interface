import pandas as pd
import matplotlib.pyplot as plt
from utils import *

# full plotter of all the things
def plot_hist_sensors_robot(file_slip = None, file_robot = None, file_load = None):
    if None in (file_slip, file_robot, file_load):
        if file_slip is not None:
            df_slip = rel_time(file_slip, 'Time')
        if file_load is not None:
            df_load = rel_time(file_load, 'Timestamp')
        if file_robot is not None:
            df_robot = rel_time(file_robot, 'Time')
    else:
        df_slip, df_load, df_robot = synch(file_slip, file_robot, file_load)    

    plt.figure(figsize=(8,4))
    if file_slip is not None:
        df_slip['contact'] = df_slip['contact'].apply(lambda x: 1 if x >0 else 0)
        plot_slip(df_slip)
    if file_load is not None:
        plot_lc(df_load)
    if file_robot is not None:
        plot_robot(df_robot)
    plt.xlabel('Time (s)')
    plt.ylabel('Sensor Values')
    plt.grid(True)
    plt.legend(loc = 2)
    plt.savefig("figs/test_hist_sensors_robot.png")
    plt.show()
        
def subplot_hist_sensors_robot(ax, file_slip = None, file_robot = None, file_load = None):
    if None in (file_slip, file_robot, file_load):
        if file_slip is not None:
            df_slip = rel_time(file_slip, 'Time')
        if file_load is not None:
            df_load = rel_time(file_load, 'Timestamp')
        if file_robot is not None:
            df_robot = rel_time(file_robot, 'Time')
    else:
        df_slip, df_load, df_robot = synch(file_slip, file_robot, file_load) 
    if file_slip is not None:
        ax.plot(df_slip['Time_rel'],df_slip['contact']*5, label = 'contact', color = 'g')
        ax.plot(df_slip['Time_rel'], df_slip['delta_X'], label='delta_X', color = 'teal')
        ax.plot(df_slip['Time_rel'], df_slip['delta_Y'], label='delta_Y', color = 'blue')
    if file_load is not None:
        ax.plot(df_load['Time_rel'],df_load['Shear_Force'], label = 'LC Shear Force', color = 'orange')
        ax.plot(df_load['Time_rel'],df_load['Normal_Force'], label = 'LC Normal Force', color = 'coral')
    if file_robot is not None:
        ax.plot(df_robot['Time_rel'],df_robot['TCP_x']*100, label = 'arm pos in x', color = 'm')
        ax.plot(df_robot['Time_rel'],df_robot['TCP_y']*100, label = 'arm pos in y', color = 'pink')
        ax.plot(df_robot['Time_rel'],df_robot['TCP_z']*100, label = 'arm pos in z', color = 'purple')
    ax.set_ylim([-10,10])
    return ax

# plot histogram only sensor
def plot_hist_slip(file):
    df_log = pd.read_csv(file)
    df_log['Time'] = pd.to_datetime(df_log['Time'], format='%Y-%m-%d %H:%M:%S.%f')
    df_log['Time_rel'] = (df_log['Time'] - df_log['Time'].iloc[0]).dt.total_seconds()
    plt.figure(figsize=(8,4))
    plot_slip(df_log)
    plt.xlabel('Time (s)')
    plt.ylabel('Delta Values')
    plt.title('x and y deltas over time')
    plt.grid(True)
    plt.legend()
    plt.savefig("figs/deltahist_sensor.png")
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

def plot_average(file_slip, file_robot = None, file_load = None,):
    df_slip, df_load, df_robot = synch(file_slip, file_robot, file_load) 
    df_slip['contact'] = df_slip['contact'].apply(lambda x: 1 if x >0 else 0)
    df_slip = moving_averge(df_slip, 10)   
    plot_slip(df_slip)
    plot_robot(df_robot)
    plot_lc(df_load)
    plt.legend()
    plt.show()


def plot_lc(df_load):
    plt.plot(df_load['Time_rel'],df_load['Shear_Force']/1000*9.81, label = 'LC Shear Force [0.1 N]', color = 'orange')
    plt.plot(df_load['Time_rel'],df_load['Normal_Force']/1000*9.81, label = 'LC Normal Force [1 N]', color = 'coral')

def plot_slip(df_slip):
    plt.plot(df_slip['Time_rel'],df_slip['contact']*5, label = 'contact', color = 'g')
    plt.plot(df_slip['Time_rel'], df_slip['delta_X'], label='delta_X', color = 'teal')
    plt.plot(df_slip['Time_rel'], df_slip['delta_Y'], label='delta_Y', color = 'blue')

def plot_robot(df_robot):
    plt.plot(df_robot['Time_rel'],df_robot['TCP_x']*100, label = 'arm pos in x', color = 'm')
    plt.plot(df_robot['Time_rel'],df_robot['TCP_y']*100, label = 'arm pos in y', color = 'pink')
    plt.plot(df_robot['Time_rel'],df_robot['TCP_z']*100, label = 'arm pos in z', color = 'purple')
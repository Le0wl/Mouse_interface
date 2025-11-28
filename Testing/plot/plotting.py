import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import *

contact_thresh = 5
slip_thresh = 5

# full plotter of all the things
def plot_hist_sensors_robot(file_slip = None, file_robot = None, file_load = None):
    df_slip, df_load, df_robot = synch(file_slip, file_robot, file_load)  

    plt.figure(figsize=(12,4))
    if file_slip is not None:
        # plot_mvt(df_slip)
        plot_slip(df_slip)

    if file_robot is not None:
        # plot_robot(df_robot)

        plot_robot_speed(df_robot)
    if file_load is not None:
        plot_shear(df_load)

    plt.xlabel('Time (s)')
    plt.ylabel('Sensor Values')
    plt.grid(True)
    plt.legend()
    plt.savefig("figs/test_hist_sensors_robot.png")
    plt.show()
        
def subplot_hist_sensors_robot(ax, file_slip = None, file_robot = None, file_load = None):
    df_slip, df_load, df_robot = synch(file_slip, file_robot, file_load)   
    if file_slip is not None:
        ax.plot(df_slip['Time_rel'],df_slip['contact']*5, label = 'contact', color = 'g')
        ax.plot(df_slip['Time_rel'], df_slip['delta_X'], label='delta_X', color = 'teal')
        ax.plot(df_slip['Time_rel'], df_slip['delta_Y'], label='delta_Y', color = 'blue')
    if file_load is not None:
        ax.plot(df_load['Time_rel'],df_load['Shear_Force'], label = 'LC Shear Force', color = 'orange')
        if "Normal_Force" in df_load.columns:
            ax.plot(df_load['Time_rel'],df_load['Normal_Force'], label = 'LC Normal Force', color = 'coral')
    if file_robot is not None:
        ax.plot(df_robot['Time_rel'],df_robot['TCP_x']*100, label = 'arm pos in x[cm]', color = 'm')
        ax.plot(df_robot['Time_rel'],df_robot['TCP_y']*100, label = 'arm pos in y[cm]', color = 'pink')
        ax.plot(df_robot['Time_rel'],df_robot['TCP_z']*100, label = 'arm pos in z[cm]', color = 'purple')
    ax.set_ylim([-20,20])
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

def plot_shear(df_load):
    if 'deriv' in df_load.columns:
            plt.plot(df_load['Time_rel'],df_load['deriv'], label = 'derviative Shear [1 N/s]', color = 'coral')
    plt.plot(df_load['Time_rel'],df_load['Shear_Force']/1000*9.81 * 10, label = 'LC Shear Force [0.1 N]', color = 'orange')

def plot_lc(df_load):
    plt.scatter(df_load['Time_rel'],df_load['Shear_Force']/1000*9.81 * 10, label = 'LC Shear Force [0.1 N]', color = 'orange', marker= '+')
    plt.scatter(df_load['Time_rel'],df_load['Normal_Force']/1000*9.81, label = 'LC Normal Force [1 N]', color = 'coral', marker= '+')

def plot_slip(df_slip):
    df_slip['contact'] = df_slip['contact'].apply(lambda x: 1 if x >contact_thresh else 0)
    plt.plot(df_slip['Time_rel'],df_slip['contact']*5, label = 'contact', color = 'g')
    plt.plot(df_slip['Time_rel'], df_slip['delta_X'], label='delta_X', color = 'teal')
    plt.plot(df_slip['Time_rel'], df_slip['delta_Y'], label='delta_Y', color = 'blue')

def plot_mvt(df_slip):
    df_slip['mvt'] = np.sqrt(df_slip['delta_X'] **2 + df_slip['delta_Y']**2)
    df_slip['contact'] = df_slip['contact'].apply(lambda x: 1 if x > contact_thresh else 0)
    plt.plot(df_slip['Time_rel'],df_slip['contact']*5, label = 'contact', color = 'g')
    plt.plot(df_slip['Time_rel'], df_slip['mvt'], label='mvt', color = 'blue')


def plot_robot(df_robot):
    plt.plot(df_robot['Time_rel'],df_robot['TCP_x']*100, label = 'arm pos in x [cm]', color = 'm')
    plt.plot(df_robot['Time_rel'],df_robot['TCP_y']*100, label = 'arm pos in y [cm]', color = 'pink')
    plt.plot(df_robot['Time_rel'],df_robot['TCP_z']*100, label = 'arm pos in z [cm]', color = 'purple')

def plot_robot_speed(df_robot):
    df_robot['d_x'], df_robot['d_y'], df_robot['d_z'] = arm_speed(df_robot)
    plt.plot(df_robot['Time_rel'],df_robot['d_x'], label = 'arm speed in x [cm/s]', color = 'm')
    plt.plot(df_robot['Time_rel'],df_robot['d_y'], label = 'arm speed in y [cm/s]', color = 'blue')
    plt.plot(df_robot['Time_rel'],df_robot['d_z'], label = 'arm speed in z [cm/s]', color = 'purple')

def comare(path_list):
    tot = len(path_list)
    fig, axs = plt.subplots(tot, 1, sharex=True, figsize=(10,4*tot))
    for i in range(tot):
        slip = path_list[i].slip
        rob = path_list[i].robo
        load = path_list[i].load
        subplot_hist_sensors_robot(file_slip=slip,file_robot=rob, file_load=load, ax=axs[i])
        axs[i].set_title(f"plot{i}")
    axs[0].legend(loc="upper right")
    fig.suptitle('tracking on different surfaces (100Hz)')
    fig.supxlabel('time [s]')
    fig.supylabel('sensor values')
    fig.savefig("figs/test_sensor_robot_compare_test.png")
    plt.show()
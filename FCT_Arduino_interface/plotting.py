import pandas as pd
import matplotlib.pyplot as plt
# import numpy as np
import os
# import csv

# plot histogram
def plot_hist(file):
    df_log = pd.read_csv(file)
    df_log['Time'] = pd.to_datetime(df_log['Time'], format='%Y-%m-%d %H:%M:%S.%f')
    df_log['Time_rel'] = (df_log['Time'] - df_log['Time'].iloc[0]).dt.total_seconds()
    df_log['contact']
    plt.figure(figsize=(8,4))
    plt.plot(df_log['Time_rel'],df_log['contact']*5, label = 'contact', color = 'g')
    plt.plot(df_log['Time_rel'], df_log['delta_X'], label='delta_X', color = 'orange')
    plt.plot(df_log['Time_rel'], df_log['delta_Y'], label='delta_Y', color = 'blue')
    plt.plot(df_log['Time_rel'],df_log['Motion_x']*100, label = 'arm movement in x', color = 'cyan')
    plt.plot(df_log['Time_rel'],df_log['Motion_y']*100, label = 'arm movement in y', color = 'pink')
    plt.plot(df_log['Time_rel'],df_log['Motion_z']*100, label = 'arm movement in z', color = 'purple')
    plt.xlabel('Time (s)')
    plt.ylabel('Delta Values')
    plt.title('x and y deltas over time')
    plt.grid(True)
    plt.legend()
    plt.savefig("figs/deltahist.png")
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

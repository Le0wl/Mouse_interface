import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import csv

path_log = 'logs/'

df_log = pd.read_csv(path_log + 'sensor_log_20251022_145345.csv')

# plot 2D path
df_log['x'] = df_log['delta_X'].cumsum()
df_log['y'] = df_log['delta_Y'].cumsum()

plt.figure(figsize=(6,6))
plt.plot(df_log['x'], df_log['y'], color='blue')
plt.xlabel('X position (pixels or counts)')
plt.ylabel('Y position (pixels or counts)')
plt.title('2D Motion Path from Sensor Deltas')
plt.axis('equal')  
plt.grid(True)
plt.tight_layout()
plt.savefig("figs/path.png")
plt.show()

# plot 2D path in mm
df_log['x'] = df_log['x']/32 * -1 #conversion determined empirically not precise
df_log['y'] = df_log['y']/32 * -1

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

# plot deltas
plt.figure(figsize=(6,6))
plt.plot(df_log['delta_X'], df_log['delta_Y'], color='red')
plt.xlabel('X position (pixels or counts)')
plt.ylabel('Y position (pixels or counts)')
plt.title('2D Motion Path from Sensor Deltas')
plt.axis('equal')   
plt.savefig("figs/deltapath.png")
plt.show()

# plot histogram
df_log['Time'] = pd.to_datetime(df_log['Time'], format='%H:%M:%S.%f')
df_log['Time_rel'] = (df_log['Time'] - df_log['Time'].iloc[0]).dt.total_seconds()

plt.figure(figsize=(6,6))
plt.plot(df_log['Time_rel'], df_log['delta_X'], label='delta_X')
plt.plot(df_log['Time_rel'], df_log['delta_Y'], label='delta_Y')
plt.xlabel('Time (s)')
plt.ylabel('Delta Values')
plt.grid(True)
plt.savefig("figs/deltahist.png")
plt.show()
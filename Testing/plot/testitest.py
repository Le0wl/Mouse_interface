from plotting import *
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

def print_freq(path, col):
    df = pd.read_csv(path)
    try:
        df[col] = pd.to_datetime(df[col], format='%Y-%m-%d %H:%M:%S.%f')
        dt = df[col].diff().dt.total_seconds()
        print("Average frequnecy: ", round(1/dt.mean(),2),"Hz", "\nstd deviation: ", round((1/dt).std(),2) ,"Hz")
    except:
        df[col] = pd.to_numeric(df[col])
        dt = df[col].diff()/1000000
        print("Average frequnecy: ", round(1/dt.mean(),2),"Hz", "\nstd deviation: ", round((1/dt).std(),2) ,"Hz")
        print("missing unit converstion")

def moving_averge(path):
    df = rel_time(path)
    df['avg_x'] = df['delta_X'].rolling(20).mean()
    df['avg_y'] = df['delta_Y'].rolling(20).mean()
    df['avg_c'] = df['contact'].rolling(20).mean()
    df['x_og'] = df['delta_X'].cumsum()/32 * -1 
    df['y_og'] = df['delta_Y'].cumsum()/32 * -1
    df['x'] = df['avg_x'].cumsum()/32 * -1 
    df['y'] = df['avg_y'].cumsum()/32 * -1
    df = df.fillna(0)

    plt.plot(df['Time_rel'],df['avg_x'], label = "avg_x", marker= '.')
    plt.plot(df['Time_rel'],df['avg_y'], label = "avg_y", marker= '.')
    plt.plot(df['Time_rel'],df['avg_c'], label = "avg_c", marker= '.')
    plt.legend()
    plt.show()

    plt.plot(df['x_og'], df['y_og'], color='red')
    plt.plot(df['x'], df['y'], color='green')
    plt.axis('equal')  
    plt.show()

path = 'logs/load_log_2025-11-21_16-24-44test.csv'
path2 = 'logs/slip_log_2025-11-21_16-24-44test.csv'
path3 = 'logs/robot_log_2025-11-21_16-24-44test.csv'
print_freq(path, 'Timestamp')
plot_hist_sensors_robot(file_load=path, file_slip=path2, file_robot=path3)


    












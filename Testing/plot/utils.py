import pandas as pd
import numpy as np
import datetime as dt
from typing import NamedTuple

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

def moving_averge(df, window):
    df['delta_X'] = df['delta_X'].rolling(window).mean()
    df['delta_Y'] = df['delta_Y'].rolling(window).mean()
    df['contact'] = df['contact'].rolling(window).mean()
    if 'mvt' in df.columns:
       df['mvt'] = df['mvt'].rolling(window).mean() 
    df = df.fillna(0)
    return df

def rel_time(filename, col):
    df = pd.read_csv(filename)
    df[col] = pd.to_datetime(df[col], format='%Y-%m-%d %H:%M:%S.%f')
    df['Time_rel'] = (df[col] - df[col].iloc[0]).dt.total_seconds()
    return df

def convert_time_format(filename, col):
    df = pd.read_csv(filename)
    df[col] = pd.to_datetime(df[col], format='%Y-%m-%d %H:%M:%S.%f')
    start_time = df[col].iloc[0]
    return df, start_time

def synch(file_slip = None, file_robot= None, file_load = None):
    starts = []
    if file_slip is not None:
        df_slip, start_slip = convert_time_format(file_slip, 'Time')
        starts.append(start_slip)
    if file_load is not None:
        df_load, start_load = convert_time_format(file_load, 'Timestamp')
        starts.append(start_load)
    if file_robot is not None:
        df_robot, start_robot = convert_time_format(file_robot, 'Time')
        starts.append(start_robot)
    t0 = min(starts)
    try:
        df_slip['Time_rel'] = (df_slip['Time'] - t0).dt.total_seconds()
    except:
        df_slip = None
    try:
        df_load['Time_rel'] = (df_load['Timestamp'] - t0).dt.total_seconds()
    except:
        df_load = None
    try: 
        df_robot['Time_rel'] = (df_robot['Time'] - t0).dt.total_seconds()
    except:
        df_robot= None
    return df_slip, df_load, df_robot

def shear_derivative(df_load):
    diff = df_load['Shear_Force'].diff()/1000*9.81
    dt = df_load['Timestamp'].diff().dt.total_seconds()
    derivative = diff/dt
    return derivative

def arm_speed(df_robot):
    diff_x = df_robot['TCP_x'].diff()*100
    diff_y = df_robot['TCP_y'].diff()*100
    diff_z = df_robot['TCP_z'].diff()*100
    dt = df_robot['Time'].diff().dt.total_seconds()
    deri_x = diff_x/dt
    deri_y = diff_y/dt
    deri_z = diff_z/dt
    return deri_x, deri_y, deri_z
    
class Paths(NamedTuple):
    slip: str
    load: str
    robo: str

def get_all_paths(path):
    if "slip" in path:
        path_sl = path
        path_ld = path_sl.replace("slip", "load")
        path_ro = path_sl.replace("slip", "robot")
    elif "load" in path:
        path_ld = path
        path_sl = path_ld.replace("load", "slip")
        path_ro = path_ld.replace("load", "robot")
    elif "robot" in path:
        path_ro = path
        path_ld = path_ro.replace("robot", "load")
        path_sl = path_ro.replace("robot", "slip")
    else:
        print("ERROR: no valid path")
        return
    all_paths = Paths(path_sl, path_ld, path_ro)
    return all_paths

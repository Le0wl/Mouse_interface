from plotting import *
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
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

def synch(file_slip, file_robot, file_load):
    df_slip, start_slip = convert_time_format(file_slip, 'Time')
    df_load, start_load = convert_time_format(file_load, 'Timestamp')
    df_robot, start_robot = convert_time_format(file_robot, 'Time')
    starts = [start_slip, start_load, start_robot]
    starts.sort()
    df_slip['Time_rel'] = (df_slip['Time'] - starts[0]).dt.total_seconds()
    df_load['Time_rel'] = (df_load['Timestamp'] - starts[0]).dt.total_seconds()
    df_robot['Time_rel'] = (df_robot['Time'] - starts[0]).dt.total_seconds()
    return df_slip, df_load, df_robot

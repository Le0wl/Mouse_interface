import pandas as pd
import numpy as np
import datetime as dt
from typing import NamedTuple
import os.path

contact_thresh = 50
slip_thresh_mouse = 5
slip_thresh_ls = 5

class Paths(NamedTuple):
    slip: str
    load: str
    robo: str

class MarkerPaths(NamedTuple):
    m1: str
    m2: str
    m3: str
    m4: str


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
    if df.empty:
        return None, None
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

def vid_synch(slip_path, m1_path,  m2_path,  m3_path,  m4_path):
    starts = []
    df_slip, start_slip = convert_time_format(slip_path, 'Time')
    starts.append(start_slip)
    df_marker = marker_panda(m1_path,  m2_path,  m3_path,  m4_path)
    start_marker = df_marker["Timestamp"].iloc[0]
    starts.append(start_marker)
    
    t0 = min(starts)
    print(starts, 'earliest:', t0)
    try:
        df_slip['Time_rel'] = (df_slip['Time'] - t0).dt.total_seconds()
    except:
        df_slip = None
    try:
        df_marker['Time_rel'] = (df_marker['Timestamp'] - t0).dt.total_seconds()
    except:
        df_marker = None

    return df_slip, df_marker

def shear_derivative(df_load):
    diff = df_load['Shear_Force'].diff()/1000*9.81
    dt = df_load['Timestamp'].diff().dt.total_seconds()
    derivative = diff/dt
    df_load['deriv'] = derivative

def arm_speed(df_robot):
    diff_x = df_robot['TCP_x'].diff()*100
    diff_y = df_robot['TCP_y'].diff()*100
    diff_z = df_robot['TCP_z'].diff()*100
    dt = df_robot['Time'].diff().dt.total_seconds()
    deri_x = diff_x/dt
    deri_y = diff_y/dt
    deri_z = diff_z/dt
    return deri_x, deri_y, deri_z
    
def get_all_paths(path):
    if "slip/slip" in path:
        path_sl = path
        path_ld = path_sl.replace("slip/slip", "loadcell/load")
        path_ro = path_sl.replace("slip/slip", "robot/robot")
    elif "loadcell/" in path:
        path_ld = path
        path_sl = path_ld.replace("loadcell/load", "slip/slip")
        path_ro = path_ld.replace("loadcell/load", "robot/robot")
    elif "robot/" in path:
        path_ro = path
        path_ld = path_ro.replace("robot/robot", "laodcell/load")
        path_sl = path_ro.replace("robot/robot", "slip/slip")
    elif "sensor" in path:
        path_sl = path
        path_ld = path_sl.replace("slip/sensor", "loadcell/load")
        path_ro = path_sl.replace("slip/sensor", "robot/robot")
    else:
        print("ERROR: no valid path")
        return
    
    if not os.path.isfile(path_sl):
        path_sl = None
    if not os.path.isfile(path_ld):
        path_ld = None
    if not os.path.isfile(path_ro):
        path_ro = None
    all_paths = Paths(path_sl, path_ld, path_ro)
    return all_paths

def get_all_markers(path):
    if "_1_" in path:
        m1 = path
        m2 = path.replace("_1_", "_2_")
        m3 = path.replace("_1_", "_3_")
        m4 = path.replace("_1_", "_4_")
    elif "_2_" in path:
        m1 = path.replace("_2_", "_1_")
        m2 = path
        m3 = path.replace("_2_", "_3_")
        m4 = path.replace("_2_", "_4_")
    elif "_3_" in path:
        m1 = path.replace("_3_", "_1_")
        m2 = path.replace("_3_", "_2_")
        m3 = path
        m4 = path.replace("_3_", "_4_")
    elif "_4_" in path:
        m1 = path.replace("_4_", "_1_")
        m2 = path.replace("_4_", "_2_")
        m3 = path.replace("_4_", "_3_")
        m4 = path
    else:
        print("ERROR: no valid path")
        return
    
    if not os.path.isfile(m1):
        m1 = None
    if not os.path.isfile(m2):
        m2 = None
    if not os.path.isfile(m3):
        m3 = None
    if not os.path.isfile(m4):
        m4 = None
    all_paths = MarkerPaths(m1, m2, m3, m4)
    return all_paths

def preprocessing(file_slip = None, file_robot= None, file_load = None):
    df_slip, df_load, df_robot = synch(file_slip, file_robot, file_load)
    shear_derivative(df_load)
    arm_speed(df_robot)
    moving_averge(df_slip, 5)
    return df_slip, df_load, df_robot 


def marker_data_pross(log1, log2, log3, log4):
    df1= pd.read_csv(log1)
    df2= pd.read_csv(log2)
    df3= pd.read_csv(log3)
    df4= pd.read_csv(log4)
    period = (1/180) # recorded at 180 fps
    df1['Time_rel'] = (df1['frame'] * period)
    df2['Time_rel'] = (df2['frame'] * period)
    df3['Time_rel'] = (df3['frame'] * period)
    df4['Time_rel'] = (df4['frame'] * period)
    
    merged = df1.merge(df2, on="frame", how="outer", suffixes=("_m1", "_m2"))
    # Compute dx, dy (will automatically be NaN when one marker is missing)
    merged["dx"] = merged["x_m2"] - merged["x_m1"]
    merged["dy"] = merged["y_m2"] - merged["y_m1"]
    scale = 24 /np.sqrt((merged["dx"].mean())**2+(merged["dy"].mean())**2) # transforms pixels to mm
    df1['x'] = df1['x'] * scale
    df1['y'] = df1['y'] * scale
    df2['x'] = df2['x'] * scale
    df2['y'] = df2['y'] * scale
    df3['x'] = df3['x'] * scale
    df3['y'] = df3['y'] * scale
    df4['x'] = df4['x'] * scale
    df4['y'] = df4['y'] * scale
    return df1, df2, df3, df4

def marker_speed(df):
    diff_x = df['x'].diff()
    diff_y = df['y'].diff()
    dt = df['Time_rel'].diff()
    deri_x = diff_x/dt
    deri_y = diff_y/dt
    return deri_x, deri_y


def marker_panda(*files):
    period = (1/180) # recorded at 180 fps
    dfs = [pd.read_csv(f) for f in files]
    
    # full set of frames across all markers
    all_frames = sorted(set().union(*[df["Timestamp"].tolist() for df in dfs]))

    # merge each dataframe into a single timeline, keeping NaN where marker missing
    merged = pd.DataFrame({"Timestamp": all_frames})
    for i, df in enumerate(dfs):
        merged = merged.merge(df[["Timestamp","x","y"]].rename(
            columns={"x":f"x{i}", "y":f"y{i}"}),
            on="Timestamp", how="left"
        )
    df = merged.copy()
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S.%f')
    start = df.index.get_loc(df['x3'].first_valid_index())
    df.drop(index=df.index[:start], axis=0, inplace=True)
    # df[['x0','y0','x1','y1','x2','y2','x3','y3']] = df[['x0','y0','x1','y1','x2','y2','x3','y3']].interpolate(method='index')
    # static point x3,y3


    for i in range(len(files)):  
        df[f"dx{i}"] = df[f"x{i}"] - get_starting_pos(df[f"x{i}"])

    df = df.reset_index()
    print(df.head(5))
    df.to_csv("test", index=False)
    return df
    
    
def get_starting_pos(col):
    start = col.index.get_loc(col.first_valid_index())
    start_pos = col.iloc[start]
    return start_pos
    

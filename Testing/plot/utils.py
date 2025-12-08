import pandas as pd
import numpy as np
import datetime as dt
from typing import NamedTuple
import os.path

contact_thresh = 50
slip_thresh_mouse = 0.3
slip_thresh_cam = 50
# slip_thresh_ls = 1
window = 5

class Paths(NamedTuple):
    slip: str
    load: str
    robo: str

class MarkerPaths(NamedTuple):
    m1: str
    m2: str
    m3: str
    m4: str
    time: str


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

def vid_synch(slip_path, m1_path,  m2_path,  m3_path,  m4_path, mtime_path):
    starts = []
    df_slip, start_slip = convert_time_format(slip_path, "Sync_Time")
    starts.append(start_slip)
    df_marker = marker_panda(m1_path,  m2_path,  m3_path,  m4_path, mtime_path)
    start_marker = df_marker["Timestamp"].iloc[0]
    starts.append(start_marker)

    slip_min, slip_max = df_slip["Sync_Time"].min(), df_slip["Sync_Time"].max()
    mark_min, mark_max = df_marker["Timestamp"].min(), df_marker["Timestamp"].max()

    # overlapping interval
    t_start = max(slip_min, mark_min)
    t_end   = min(slip_max, mark_max)

    # trim to overlap
    df_slip_cut = df_slip[(df_slip["Sync_Time"] >= t_start) & (df_slip["Sync_Time"] <= t_end)].copy()
    df_marker_cut = df_marker[(df_marker["Timestamp"] >= t_start) & (df_marker["Timestamp"] <= t_end)].copy()
        
    return df_slip_cut, df_marker_cut

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
        time = path.replace("marker_1", "time")
    elif "_2_" in path:
        m1 = path.replace("_2_", "_1_")
        m2 = path
        m3 = path.replace("_2_", "_3_")
        m4 = path.replace("_2_", "_4_")
        time = path.replace("marker_2", "time")
    elif "_3_" in path:
        m1 = path.replace("_3_", "_1_")
        m2 = path.replace("_3_", "_2_")
        m3 = path
        m4 = path.replace("_3_", "_4_")
        time = path.replace("marker_3", "time")
    elif "_4_" in path:
        m1 = path.replace("_4_", "_1_")
        m2 = path.replace("_4_", "_2_")
        m3 = path.replace("_4_", "_3_")
        m4 = path
        time = path.replace("marker_4", "time")
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
    if not os.path.isfile(time):
        time = None
    all_paths = MarkerPaths(m1, m2, m3, m4, time)
    return all_paths

def preprocessing(file_slip = None, file_robot= None, file_load = None):
    df_slip, df_load, df_robot = synch(file_slip, file_robot, file_load)
    shear_derivative(df_load)
    arm_speed(df_robot)
    moving_averge(df_slip, 5)
    return df_slip, df_load, df_robot 




# aligning frames and time
def marker_panda(*files):
    dfs = []
    for f in files:
        try:
            df = pd.read_csv(f)
            dfs.append(df)
        except:
            dfs.append(None)
    df_time = dfs[-1]
    df_markers = dfs[:-1]
    df_time["frame"] = df_time["frame_id"]

    # merge each dataframe into a single timeline, keeping NaN where marker missing
    merged = df_time.copy() 
    for i, df in enumerate(df_markers): 
        merged = merged.merge(df[["frame","x","y"]].rename(
            columns={"x":f"x{i}", "y":f"y{i}"}),
            on="frame", how="left"
        )
    df = merged.copy()
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S.%f')
    start = df.index.get_loc(df['x3'].first_valid_index())
    df.drop(index=df.index[:start], axis=0, inplace=True)
    # static point x3,y3 added to the frame then setup is ready

    for i in range(len(df_markers)):  
        df[f"dx{i}"] = df[f"x{i}"] - get_starting_pos(df[f"x{i}"])
    
    df= get_speed(df)

    df = df.reset_index()
    df.to_csv("test", index=False)
    return df
    
    
def get_starting_pos(col):
    start = col.index.get_loc(col.first_valid_index())
    start_pos = col.iloc[start]
    return start_pos


def get_speed(df):
    col = df["dx2"].copy()
    col.index = pd.to_datetime(df["Timestamp"])
    col_smooth = col.interpolate(method='time')
    col_smooth = col_smooth.rolling(window).mean()
    df = df.set_index("Timestamp")  # key fix

    dt = col_smooth.index.to_series().diff().dt.total_seconds()
    df["speed"] = col_smooth.diff() / dt

    df["slip"] = (np.abs(df["speed"]) > slip_thresh_cam).astype(int)
    return df

def slip_detection(df):
    df['contact'] = df['contact'].rolling(window).mean() 
    df['contact'] = df['contact'].apply(lambda x: True if x >contact_thresh else False)
    df['mvt'] = np.sqrt(df['delta_X'] **2 + df['delta_Y']**2)
    df['mvt'] = df['mvt'].rolling(window).mean() 
    df['slip'] = df['mvt'].apply(lambda x: True if x > slip_thresh_mouse else False)
    df['slip'] = df['slip'] & df['contact']
    return df
  

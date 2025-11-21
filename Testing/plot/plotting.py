import pandas as pd
import matplotlib.pyplot as plt

# # plot histogram sensor and arm
# def plot_hist_sensor_robot(file, file2, ax = None):
#     df_log = pd.read_csv(file)
#     df_log2 = pd.read_csv(file2)
#     df_log['Time'] = pd.to_datetime(df_log['Time'], format='%Y-%m-%d %H:%M:%S.%f')
#     df_log['Time_rel'] = (df_log['Time'] - df_log['Time'].iloc[0]).dt.total_seconds()

#     df_log2['Time'] = pd.to_datetime(df_log2['Time'], format='%Y-%m-%d %H:%M:%S.%f')
#     df_log2['Time_rel'] = (df_log2['Time'] - df_log2['Time'].iloc[0]).dt.total_seconds()

#     df_log['contact']
#     if ax is None: 
#         plt.figure(figsize=(8,4))
#         plt.plot(df_log['Time_rel'],df_log['contact']*5, label = 'contact', color = 'g')
#         plt.plot(df_log['Time_rel'], df_log['Movement'], label='Movement', color = 'cyan')
#         plt.plot(df_log['Time_rel'], df_log['delta_X'], label='delta_X', color = 'orange')
#         plt.plot(df_log['Time_rel'], df_log['delta_Y'], label='delta_Y', color = 'blue')

#         plt.plot(df_log2['Time_rel'],df_log2['TCP_x']*100, label = 'arm pos in x', color = 'm')
#         plt.plot(df_log2['Time_rel'],df_log2['TCP_y']*100, label = 'arm pos in y', color = 'pink')
#         plt.plot(df_log2['Time_rel'],df_log2['TCP_z']*100, label = 'arm pos in z', color = 'purple')
#         plt.xlabel('Time (s)')
#         plt.ylabel('Sensor Values')
#         plt.grid(True)
#         plt.legend()
#         plt.savefig("figs/deltahist_sensor_robot.png")
#         plt.show()
#     else:
#         ax.plot(df_log['Time_rel'],df_log['contact']*5, label = 'contact', color = 'g')
#         ax.plot(df_log['Time_rel'], df_log['delta_X'], label='delta_X', color = 'orange')
#         ax.plot(df_log['Time_rel'], df_log['delta_Y'], label='delta_Y', color = 'blue')

#         ax.plot(df_log2['Time_rel'],df_log2['TCP_x']*100, label = 'arm pos in x', color = 'cyan')
#         ax.plot(df_log2['Time_rel'],df_log2['TCP_y']*100, label = 'arm pos in y', color = 'pink')
#         ax.plot(df_log2['Time_rel'],df_log2['TCP_z']*100, label = 'arm pos in z', color = 'purple')
#         ax.set_ylim([-10,10])
#         return ax

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


def plot_hist_sensors_robot(file_slip = None, file_robot = None, file_load = None, ax = None):

    if None in (file_slip, file_robot, file_load):
        if file_slip is not None:
            df_slip = rel_time(file_slip, 'Time')
            # df_slip['contact']
        if file_load is not None:
            df_load = rel_time(file_load, 'Timestamp')

        if file_robot is not None:
            df_robot = rel_time(file_robot, 'Time')
    else:
        df_slip, df_load, df_robot = synch(file_slip, file_robot, file_load)    
    if ax is None: 
        plt.figure(figsize=(8,4))
        if file_slip is not None:
            # plt.plot(df_slip['Time_rel'],df_slip['contact']/5, label = 'contact', color = 'g')
            # if 'Movement' in df_slip.columns:
            #     plt.plot(df_slip['Time_rel'], df_slip['Movement'], label='Movement', color = 'cyan')
            plt.plot(df_slip['Time_rel'], df_slip['delta_X'], label='delta_X', color = 'teal')
            plt.plot(df_slip['Time_rel'], df_slip['delta_Y'], label='delta_Y', color = 'blue')
        if file_load is not None:
            plt.plot(df_load['Time_rel'],df_load['Shear_Force']/100*9.81, label = 'LC Shear Force [0.1 N]', color = 'orange')
            plt.plot(df_load['Time_rel'],df_load['Normal_Force']/1000*9.81, label = 'LC Normal Force [1 N]', color = 'coral')
        if file_robot is not None:
            plt.plot(df_robot['Time_rel'],df_robot['TCP_x']*100, label = 'arm pos in x', color = 'm')
            plt.plot(df_robot['Time_rel'],df_robot['TCP_y']*100, label = 'arm pos in y', color = 'pink')
            plt.plot(df_robot['Time_rel'],df_robot['TCP_z']*100, label = 'arm pos in z', color = 'purple')
        plt.xlabel('Time (s)')
        plt.ylabel('Sensor Values')
        plt.grid(True)
        plt.legend(loc = 2)
        plt.savefig("figs/test_hist_sensors_robot.png")
        plt.show()
    else:
        if file_slip is not None:
            ax.plot(df_slip['Time_rel'],df_slip['contact']*5, label = 'contact', color = 'g')
            ax.plot(df_slip['Time_rel'], df_slip['Movement'], label='Movement', color = 'cyan')
            ax.plot(df_slip['Time_rel'], df_slip['delta_X'], label='delta_X', color = 'teal')
            ax.plot(df_slip['Time_rel'], df_slip['delta_Y'], label='delta_Y', color = 'blue')
        if file_load is not None:
            ax.plot(df_load['Time_rel'],df_load['Shear_Force'], label = 'LC Shear Force', color = 'orange')
            ax.plot(df_load['Time_rel'],df_load['Normal_Force'], label = 'LC Normal Force', color = 'coral')
            ax.plot(df_load['Time_rel'],df_load['Hook_Force'], label = 'LC Hook Force', color = 'peachpuff')
        if file_robot is not None:
            ax.plot(df_robot['Time_rel'],df_robot['TCP_x']*100, label = 'arm pos in x', color = 'm')
            ax.plot(df_robot['Time_rel'],df_robot['TCP_y']*100, label = 'arm pos in y', color = 'pink')
            ax.plot(df_robot['Time_rel'],df_robot['TCP_z']*100, label = 'arm pos in z', color = 'purple')
        ax.set_ylim([-10,10])
        return ax




# plot histogram only sensor
def plot_hist0(file):
    df_log = pd.read_csv(file)
    df_log['Time'] = pd.to_datetime(df_log['Time'], format='%Y-%m-%d %H:%M:%S.%f')
    df_log['Time_rel'] = (df_log['Time'] - df_log['Time'].iloc[0]).dt.total_seconds()

    df_log['contact']
    plt.figure(figsize=(8,4))
    plt.plot(df_log['Time_rel'],df_log['contact']/5, label = 'contact', color = 'g')
    plt.plot(df_log['Time_rel'], df_log['delta_X'], label='delta_X', color = 'orange')
    plt.plot(df_log['Time_rel'], df_log['delta_Y'], label='delta_Y', color = 'blue')

    plt.xlabel('Time (s)')
    plt.ylabel('Delta Values')
    plt.title('x and y deltas over time')
    plt.grid(True)
    plt.legend()
    plt.savefig("figs/deltahist_sensor.png")
    plt.show()

def plot_hist2(file):
    df_log = pd.read_csv(file)
    df_log['Time'] = pd.to_datetime(df_log['Time'], format='%Y-%m-%d %H:%M:%S.%f')
    df_log['Time_rel'] = (df_log['Time'] - df_log['Time'].iloc[0]).dt.total_seconds()
    df_log['contact']
    plt.figure(figsize=(8,4))
    plt.plot(df_log['Time_rel'],df_log['TCP_x']*100, label = 'arm pos in x', color = 'cyan')
    plt.plot(df_log['Time_rel'],df_log['TCP_y']*100, label = 'arm pos in y', color = 'pink')
    plt.plot(df_log['Time_rel'],df_log['TCP_z']*100, label = 'arm pos in z', color = 'purple')
    plt.xlabel('Time (s)')
    plt.ylabel('Delta Values')
    plt.title('x and y deltas over time')
    plt.grid(True)
    plt.legend()
    plt.savefig("figs/deltahist_robot.png")
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

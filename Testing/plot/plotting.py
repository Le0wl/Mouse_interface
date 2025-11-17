import pandas as pd
import matplotlib.pyplot as plt

# plot histogram sensor and arm
def plot_hist_sensor_robot(file, file2, ax = None):
    df_log = pd.read_csv(file)
    df_log2 = pd.read_csv(file2)
    df_log['Time'] = pd.to_datetime(df_log['Time'], format='%Y-%m-%d %H:%M:%S.%f')
    df_log['Time_rel'] = (df_log['Time'] - df_log['Time'].iloc[0]).dt.total_seconds()

    df_log2['Time'] = pd.to_datetime(df_log2['Time'], format='%Y-%m-%d %H:%M:%S.%f')
    df_log2['Time_rel'] = (df_log2['Time'] - df_log2['Time'].iloc[0]).dt.total_seconds()

    df_log['contact']
    if ax is None: 
        plt.figure(figsize=(8,4))
        plt.plot(df_log['Time_rel'],df_log['contact']*5, label = 'contact', color = 'g')
        plt.plot(df_log['Time_rel'], df_log['Movement'], label='Movement', color = 'cyan')
        plt.plot(df_log['Time_rel'], df_log['delta_X'], label='delta_X', color = 'orange')
        plt.plot(df_log['Time_rel'], df_log['delta_Y'], label='delta_Y', color = 'blue')

        plt.plot(df_log2['Time_rel'],df_log2['TCP_x']*100, label = 'arm pos in x', color = 'm')
        plt.plot(df_log2['Time_rel'],df_log2['TCP_y']*100, label = 'arm pos in y', color = 'pink')
        plt.plot(df_log2['Time_rel'],df_log2['TCP_z']*100, label = 'arm pos in z', color = 'purple')
        plt.xlabel('Time (s)')
        plt.ylabel('Sensor Values')
        plt.grid(True)
        plt.legend()
        plt.savefig("figs/deltahist_sensor_robot.png")
        plt.show()
    else:
        ax.plot(df_log['Time_rel'],df_log['contact']*5, label = 'contact', color = 'g')
        ax.plot(df_log['Time_rel'], df_log['delta_X'], label='delta_X', color = 'orange')
        ax.plot(df_log['Time_rel'], df_log['delta_Y'], label='delta_Y', color = 'blue')

        ax.plot(df_log2['Time_rel'],df_log2['TCP_x']*100, label = 'arm pos in x', color = 'cyan')
        ax.plot(df_log2['Time_rel'],df_log2['TCP_y']*100, label = 'arm pos in y', color = 'pink')
        ax.plot(df_log2['Time_rel'],df_log2['TCP_z']*100, label = 'arm pos in z', color = 'purple')
        ax.set_ylim([-10,10])
        return ax





# plot histogram only sensor
def plot_hist0(file):
    df_log = pd.read_csv(file)
    df_log['Time'] = pd.to_datetime(df_log['Time'], format='%Y-%m-%d %H:%M:%S.%f')
    df_log['Time_rel'] = (df_log['Time'] - df_log['Time'].iloc[0]).dt.total_seconds()

    df_log['contact']
    plt.figure(figsize=(8,4))
    plt.plot(df_log['Time_rel'],df_log['contact']*5, label = 'contact', color = 'g')
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

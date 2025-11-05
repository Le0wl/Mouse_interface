from plotting import *
import pandas as pd

PATH = 'logs/sensor_log_2025-11-05_17-02-18.csv'
PATH2 = 'logs/robot_log_2025-11-05_17-02-18.csv'
# plot_path(PATH)
plot_hist(PATH,PATH2)

def print_freq(path):
    df = pd.read_csv(path)
    df['Time'] = pd.to_datetime(df['Time'], format='%Y-%m-%d %H:%M:%S.%f')
    dt = df['Time'].diff().dt.total_seconds()
    print("Average frequnecy:", 1/dt.mean(), "Hz", "average deviation", dt.std()/dt.mean()*100 , "%")

print_freq(PATH)
print_freq(PATH2)




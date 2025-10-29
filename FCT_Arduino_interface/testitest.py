from plotting import *
import pandas as pd

PATH = 'logs/sensor_log_20251029_111047.csv'

plot_hist(PATH)
df = pd.read_csv(PATH)
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S.%f')
dt = df['Time'].diff().dt.total_seconds()
print("Average time interval:", dt.mean(), "s", "average deviation", dt.std()/dt.mean()*100 , "%")







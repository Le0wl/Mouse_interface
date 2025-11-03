from plotting import *
import pandas as pd

PATH = 'logs/sensor_log_20251031_153812.csv'
# plot_path(PATH)
plot_hist(PATH)
# df = pd.read_csv(PATH)
# df['Time'] = pd.to_datetime(df['Time'], format='%Y-%m-%d %H:%M:%S.%f')
# dt = df['Time'].diff().dt.total_seconds()
# print("Average time interval:", dt.median(), "s", "average deviation", dt.std()/dt.mean()*100 , "%")




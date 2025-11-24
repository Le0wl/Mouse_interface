from plotting import *
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


path_lc = 'logs/load_log_2025-11-23_19-45-44plastic.csv'
path_sl = 'logs/slip_log_2025-11-23_19-45-44plastic.csv'
path_ro = 'logs/robot_log_2025-11-23_19-45-44plastic.csv'
plot_hist_sensors_robot(file_load=path_lc, file_slip=path_sl, file_robot=path_ro)
plot_average(file_load=path_lc, file_slip=path_sl, file_robot=path_ro)




    












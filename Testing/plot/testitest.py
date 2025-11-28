from plotting import *
import pandas as pd
from datetime import datetime
from utils import *
import matplotlib.pyplot as plt


run1 = get_all_paths('logs/load_log_2025-11-24_15-43-38plastic_80hz.csv')

run2 = get_all_paths('logs/slip_log_2025-11-23_19-44-37plastic.csv')
now ='logs/load_log_2025-11-24_15-22-50testitest.csv'

run3 = get_all_paths('logs/robot_log_2025-11-23_19-50-44plastic_bad_contact.csv')

comare([run1, run2, run3])

# plot_hist_slip(path_sl)
# plot_hist_sensors_robot(file_load=run1.load, file_robot=run1.robo, file_slip=run1.slip)
# plot_average(file_load=path_lc, file_slip=path_sl, file_robot=path_ro)
# print_freq(path_sl, 'Timestamp')
# plot_load_ideas(file_lc=path_lc, file_ro=path_ro, file_sl=path_sl)






    












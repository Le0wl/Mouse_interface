from plotting import *
from utils import *



run1 = get_all_paths('logs/slip_log_2025-11-24_15-52-19plastic_80hz.csv')

run2 = get_all_paths('logs/slip_log_2025-11-23_19-44-37plastic.csv')
# now ='logs/load_log_2025-11-24_15-22-50testitest.csv'

run3 = get_all_paths('logs/robot_log_2025-11-23_19-50-44plastic_bad_contact.csv')

# compare([[run1, run2, run3]])

# plot_hist_slip(path_sl)
# plot_hist_sensors_robot(file_load=run1.load, file_robot=run1.robo, file_slip=run1.slip)
# print_freq(run1.load, 'Timestamp')
# print_freq(run2.load, 'Timestamp')
# print_freq(run3.load, 'Timestamp')

# plot_average(file_load=path_lc, file_slip=path_sl, file_robot=path_ro)
# print_freq(path_sl, 'Timestamp')
# plot_load_ideas(file_lc=path_lc, file_ro=path_ro, file_sl=path_sl)
print_freq('logs/marker_3_log.csv', 'Timestamp')
# plot_markerpos('logs/marker_1_log.csv', 'logs/marker_2_log.csv', 'logs/marker_3_log.csv', 'logs/marker_4_log.csv')

# hat = get_all_paths('logs/sensor_log_2025-11-13_11-02-34hat.csv')
# paper = get_all_paths('logs/sensor_log_2025-11-13_10-44-20paper.csv' )
# book = get_all_paths('logs/sensor_log_2025-11-13_10-49-21bookcover.csv' )
# pattern = get_all_paths('logs/sensor_log_2025-11-13_14-45-28paper_patterned.csv')

# hat_l = get_all_paths('logs/sensor_log_2025-11-13_17-22-37hat_with_lense.csv')
# paper_l = get_all_paths('logs/sensor_log_2025-11-13_17-14-35paper_with_lense.csv')
# book_l = get_all_paths('logs/sensor_log_2025-11-13_16-57-05book_with_lense.csv')
# pattern_l = get_all_paths('logs/sensor_log_2025-11-13_17-17-44pattern_paper_with_lense.csv')


# compare([[hat, paper, book, pattern], [hat_l, paper_l, book_l, pattern_l]])



    












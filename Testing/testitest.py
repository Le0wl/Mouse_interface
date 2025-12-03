from plot.plotting import *
from plot.utils import *


# run1 = get_all_paths('logs/slip_log_2025-11-24_15-52-19plastic_80hz.csv')

run2 = get_all_paths('logs/slip/slip_log_2025-11-23_19-44-37plastic.csv')
# now ='logs/load_log_2025-11-24_15-22-50testitest.csv'

run3 = get_all_paths('logs/robot/robot_log_2025-11-23_19-50-44plastic_bad_contact.csv')
run = get_all_paths('logs/slip/slip_log_2025-12-03_16-58-46sync_with_cam.csv')
markers = get_all_markers('logs/marker/marker_4_log2025-12-03_16-58-48.csv')
plot_vid_slip(run.slip, markers.m1, markers.m2, markers.m3, markers.m4)
# compare([[run2], [run3]])

# plot_hist_sensors_robot(file_load=run2.load, file_robot=run2.robo, file_slip=run2.slip)


# plot_average(file_load=path_lc, file_slip=path_sl, file_robot=path_ro)
# print_freq(path_sl, 'Timestamp')
# plot_load_ideas(file_lc=path_lc, file_ro=path_ro, file_sl=path_sl)
# print_freq('logs/marker/marker_3_log.csv', 'Timestamp')







# marker_panda('logs/marker/marker_2_log.csv', 'logs/marker/marker_3_log.csv', 'logs/marker/marker_4_log.csv')
# marker_traj()
plot_markerpos('logs/marker/marker_1_log.csv', 'logs/marker/marker_2_log.csv', 'logs/marker/marker_3_log.csv', 'logs/marker/marker_4_log.csv')
# marker_path('logs/marker/marker_1_log.csv', 'logs/marker/marker_2_log.csv', 'logs/marker/marker_3_log.csv', 'logs/marker/marker_4_log.csv')
# marker_path_animated('logs/marker/marker_2_log.csv', 'logs/marker/marker_3_log.csv', 'logs/marker/marker_4_log.csv')
# plt_marker_speed('logs/marker/marker_1_log.csv', 'logs/marker/marker_2_log.csv', 'logs/marker/marker_3_log.csv', 'logs/marker/marker_4_log.csv')







# hat = get_all_paths('logs/sensor_log_2025-11-13_11-02-34hat.csv')
# paper = get_all_paths('logs/sensor_log_2025-11-13_10-44-20paper.csv' )
# book = get_all_paths('logs/sensor_log_2025-11-13_10-49-21bookcover.csv' )
# pattern = get_all_paths('logs/sensor_log_2025-11-13_14-45-28paper_patterned.csv')

# hat_l = get_all_paths('logs/sensor_log_2025-11-13_17-22-37hat_with_lense.csv')
# paper_l = get_all_paths('logs/sensor_log_2025-11-13_17-14-35paper_with_lense.csv')
# book_l = get_all_paths('logs/sensor_log_2025-11-13_16-57-05book_with_lense.csv')
# pattern_l = get_all_paths('logs/sensor_log_2025-11-13_17-17-44pattern_paper_with_lense.csv')


# compare([[hat, paper, book, pattern], [hat_l, paper_l, book_l, pattern_l]])



    












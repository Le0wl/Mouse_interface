from plot.plotting import *
from plot.utils import *
from vision.marker_detection import *
from vision.capture import record_video
from testcase_main import *
from config import *
# run1 = get_all_paths('logs/slip_log_2025-11-24_15-52-19plastic_80hz.csv')

run2 = get_all_paths('logs/slip/slip_log_2025-11-23_19-44-37plastic.csv')
# now ='logs/load_log_2025-11-24_15-22-50testitest.csv'

run3 = get_all_paths('logs/robot/robot_log_2025-11-23_19-50-44plastic_bad_contact.csv')

# t0 = "2025-12-08_11-11-35"
# t1 = t=0

t0 = "2025-12-11_12-04-24"
t1 = "2025-12-11_12-04-25"
run = get_all_paths(f"logs/slip/slip_log_{t0}{SURFACE}.csv")
markers = get_all_markers(f"logs/marker/marker_4_log{t1}.csv")


plot_vid_slip(run.slip, markers.m1, markers.m2, markers.m3, markers.m4, markers.time)
# compare_slip_time(run.slip)

# test_detection()
# record_video("Silicon")


# plot_hist_sensors_robot(file_load=run2.load, file_robot=run2.robo, file_slip=run2.slip)

# plot_average(file_load=path_lc, file_slip=path_sl, file_robot=path_ro)
# print_freq(path_sl, 'Timestamp')
# plot_load_ideas(file_lc=path_lc, file_ro=path_ro, file_sl=path_sl)
# print_freq('logs/marker/marker_3_log.csv', 'Timestamp')


# df_m = pd.read_csv('logs/marker/marker_4_log2025-12-04_19-06-30.csv')
# df_t = pd.read_csv('logs/marker/time_log2025-12-04_19-06-30.csv')

# df_t["frame"] = df_t["frame_id"]

# merged = df_t 
# df_marker = df_t.merge(df_m[["frame", "x", "y"]], on="frame", how="left")

# df_marker['Timestamp'] = pd.to_datetime(df_marker['Timestamp'], format='%Y-%m-%d %H:%M:%S.%f')
# start = pd.to_datetime('2025-12-04 19:06:34.9', format ='%Y-%m-%d %H:%M:%S.%f')
# end = pd.to_datetime('2025-12-04 19:06:36.0', format ='%Y-%m-%d %H:%M:%S.%f')

# df_marker.to_csv('help.csv')
# plt.scatter(df_marker['Timestamp'], df_marker['x']- get_starting_pos(df_marker[f"x"]), marker = "+")
# plt.plot([start, start], [10, -200], color= "red")
# plt.plot([end, end], [10, -200], color= "red")
# plt.show()

# marker_panda('logs/marker/marker_2_log.csv', 'logs/marker/marker_3_log.csv', 'logs/marker/marker_4_log.csv')
# marker_traj()
# plot_markerpos('logs/marker/marker_1_log.csv', 'logs/marker/marker_2_log.csv', 'logs/marker/marker_3_log.csv', 'logs/marker/marker_4_log.csv')
# marker_path('logs/marker/marker_1_log.csv', 'logs/marker/marker_2_log.csv', 'logs/marker/marker_3_log.csv', 'logs/marker/marker_4_log.csv')
# marker_path_animated('logs/marker/marker_2_log.csv', 'logs/marker/marker_3_log.csv', 'logs/marker/marker_4_log.csv')
# plt_marker_speed('logs/marker/marker_1_log.csv', 'logs/marker/marker_2_log.csv', 'logs/marker/marker_3_log.csv', 'logs/marker/marker_4_log.csv')

# marker_logging('vids/video_2025-12-04_19-06-30-415852.avi')





# hat = get_all_paths('logs/sensor_log_2025-11-13_11-02-34hat.csv')
# paper = get_all_paths('logs/sensor_log_2025-11-13_10-44-20paper.csv' )
# book = get_all_paths('logs/sensor_log_2025-11-13_10-49-21bookcover.csv' )
# pattern = get_all_paths('logs/sensor_log_2025-11-13_14-45-28paper_patterned.csv')

# hat_l = get_all_paths('logs/sensor_log_2025-11-13_17-22-37hat_with_lense.csv')
# paper_l = get_all_paths('logs/sensor_log_2025-11-13_17-14-35paper_with_lense.csv')
# book_l = get_all_paths('logs/sensor_log_2025-11-13_16-57-05book_with_lense.csv')
# pattern_l = get_all_paths('logs/sensor_log_2025-11-13_17-17-44pattern_paper_with_lense.csv')


# compare([[hat, paper, book, pattern], [hat_l, paper_l, book_l, pattern_l]])



    












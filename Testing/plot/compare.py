from plotting import *
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


# PATH11 = 'logs/slip_log_2025-11-23_19-50-44plastic_bad_contact.csv'
# PATH12 = 'logs/robot_log_2025-11-23_19-50-44plastic_bad_contact.csv'
# PATH13 = 'logs/load_log_2025-11-23_19-50-44plastic_bad_contact.csv'

# PATH21 = 'logs/sensor_log_2025-11-13_10-44-20paper.csv' 
# PATH22 = 'logs/robot_log_2025-11-13_10-44-20paper.csv'

# PATH31 = 'logs/sensor_log_2025-11-13_10-49-21bookcover.csv' 
# PATH32 = 'logs/robot_log_2025-11-13_10-49-21bookcover.csv'

# PATH41 = 'logs/sensor_log_2025-11-13_14-45-28paper_patterned.csv' 
# PATH42 = 'logs/robot_log_2025-11-13_14-45-28paper_patterned.csv'

PATH011 = 'logs/sensor_log_2025-11-13_17-22-37hat_with_lense.csv'
PATH012 = 'logs/robot_log_2025-11-13_17-22-37hat_with_lense.csv'

PATH021 = 'logs/sensor_log_2025-11-13_17-14-35paper_with_lense.csv' 
PATH022 = 'logs/robot_log_2025-11-13_17-14-35paper_with_lense.csv'

PATH031 = 'logs/sensor_log_2025-11-13_16-57-05book_with_lense.csv' 
PATH032 = 'logs/robot_log_2025-11-13_16-57-05book_with_lense.csv'

PATH041 = 'logs/sensor_log_2025-11-13_17-17-44pattern_paper_with_lense.csv' 
PATH042 = 'logs/robot_log_2025-11-13_17-17-44pattern_paper_with_lense.csv'



# fig, axs = plt.subplots(4, 2, sharex=True, figsize=(10,10))
# subplot_hist_sensors_robot(file_slip=PATH11,file_robot=PATH12, file_load=PATH13, ax=axs[0,0])
# axs[0,0].set_title("without lense on fabric")
# subplot_hist_sensors_robot(file_slip=PATH21,file_robot=PATH22, ax=axs[1,0])
# axs[1,0].set_title("without lense on paper")
# subplot_hist_sensors_robot(file_slip=PATH31,file_robot=PATH32, ax=axs[2,0])
# axs[2,0].set_title("without lense on book")
# subplot_hist_sensors_robot(file_slip=PATH41,file_robot=PATH42, ax=axs[3,0])
# axs[3,0].set_title("without lense on patterned paper")
# subplot_hist_sensors_robot(file_slip=PATH011,file_robot=PATH012, ax=axs[0,1])
# axs[0,1].set_title("with lense on fabric")
# subplot_hist_sensors_robot(file_slip=PATH021,file_robot=PATH022, ax=axs[1,1])
# axs[1,1].set_title("with lense on paper")
# subplot_hist_sensors_robot(file_slip=PATH031,file_robot=PATH032, ax=axs[2,1])
# axs[2,1].set_title("with lense on book")
# subplot_hist_sensors_robot(file_slip=PATH041,file_robot=PATH042, ax=axs[3,1])
# axs[3,1].set_title("with lense on patterned paper")
# axs[0,1].legend(loc="upper right")
# fig.suptitle('tracking on different surfaces (100Hz)')
# fig.supxlabel('time [s]')
# fig.supylabel('sensor values')
# fig.savefig("figs/deltahist_sensor_robot_compare_test.png")
# plt.show()










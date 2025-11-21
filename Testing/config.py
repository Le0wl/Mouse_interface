# Configure for the setup

ARDUINO_PORT = {'slip': 'COM7', 'loadcell': 'COM9'}
BAUD_RATE = {'slip': 500000, 'loadcell': 115200}

COLUMNS = {'slip': ['Timestamp','Time', 'contact', 'delta_X', 'delta_Y'],
           'loadcell': ["Timestamp", "Shear_Force","Normal_Force"]}

#connections
CONNECTIONS = {'slip' : True, 'robot': True, 'loadcell': True }

SAVE_PATH = 'logs'
LOG_TIME = 11           # maximum logtime before terminating in seconds
PLOT = True
UR_IP = '169.254.20.10'
SURFACE = 'test'
MOVE = [                        # list of relative waypoints
    [0, -0.04, 0,  0, 0, 0], 
    [0, 0.04, 0,  0, 0, 0],
    ]
    # [0, 0, 0.04,  0, 0, 0],     # up
    # [0, 0, -0.04,  0, 0, 0],    # down
    # [0, -0.04, 0,  0, 0, 0],
    # [0, 0.04, 0,  0, 0, 0],
    # [0, 0, 0.04,  0, 0, 0],     # up
    # [0, 0, -0.035,  0, 0, 0],   # down
    # [0, -0.04, 0,  0, 0, 0],    # float at 5mm
    # [0, 0.04, 0,  0, 0, 0],
    # [0, 0, -0.005,  0, 0, 0],   # down (contact)
    # [0, -0.04, 0.01,  0, 0, 0], # diagonal up
    # [0, 0.04, 0,  0, 0, 0],     # diagonal down
    # ]

# data we get: slip vs float vs contact
# reapeat. 
# full flat (perfect contact), 
# contacting but at a slight angle (imperfect contact), 
# on the following surfaces:
# paper, plastic, fabric, silicon, semi-transparent material 


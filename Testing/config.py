# Configure for the setup

ARDUINO_PORT = {'slip': 'COM7', 'loadcell': 'COM9'}
BAUD_RATE = {'slip': 500000, 'loadcell': 115200}

COLUMNS = {'slip': ['Timestamp','Arduino_Time', 'contact', 'delta_X', 'delta_Y'],
           'loadcell': ["Timestamp", "Shear_Force"]} #normal forche after if there

#connections
CONNECTIONS = {'slip' : True, 'robot': False, 'loadcell': False, 'camera': True }

SAVE_PATH = 'logs'
LOG_TIME = 20           # maximum logtime before terminating in seconds
PLOT = False
UR_IP = '169.254.20.10'
SURFACE = 'string_roll'
CAM_FPS = 180.0
SHOW = True
MOVE = [                        # list of relative waypoints
    [0, -0.04, 0,  0, 0, 0],    # forward
    [0, 0, 0.04,  0, 0, 0],     # up (4cm)
    [0, 0.04, 0,  0, 0, 0],     # backward   
    [0, 0, -0.04,  0, 0, 0],    # down
    [0, -0.04, 0,  0, 0, 0],    # forward
    [0, 0, 0.005,  0, 0, 0],    # up (5mm)
    [0, 0.04, 0,  0, 0, 0],     # backward 
    [0, 0, -0.005,  0, 0, 0],   # down (contact)
    [0, -0.02, 0,  0, 0, 0],
    [0, -0.04, 0.01,  0, 0, 0],     # diagonal froward/up
    [0, 0.04, -0.01,  0, 0, 0],     # diagonal backward/down
    [0, 0.02, 0,  0, 0, 0],         
    ]
# setup things: arucos that are squares with sides of 15mm or more work well, 
# distance to the camera around 20-30 cm test the detection before doing a long run
# data we get: slip vs float vs contact
# reapeat. 
# full flat (perfect contact), 
# contacting but at a slight angle (imperfect contact), 
# on the following surfaces:
# wood, paper, PLA, fabric, silicon 


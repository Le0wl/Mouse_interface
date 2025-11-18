# Configure for the setup
# SLIP_ARDUINO_PORT = 'COM7'
# SLIP_BAUD_RATE = 500000

# LC_ARDUINO_PORT = 'COM1' #change
# LC_BAUD_RATE = 115200
ARDUINO_PORT = {'slip': 'COM7', 'loadcell': 'COM1'}
BAUD_RATE = {'slip': 500000, 'loadcell': 115200}

COLUMNS = {'slip': ['Timestamp','Time', 'contact', 'delta_X', 'delta_Y','Movement'],
           'loadcell': ["Timestamp", "Shear_Force","Normal_Force","Hook_Force"]}

#connections
CONNECTIONS = {'slip' : True, 'robot': False, 'loadcell': False }

SAVE_PATH = 'logs'
LOG_TIME = 10
PLOT = True
UR_IP = '169.254.20.10'
SURFACE = 'test_table'
MOVE = [
    [0, -0.04, 0,  0, 0, 0], 
    [0, 0.04, 0,  0, 0, 0],
    [0, -0.04, 0,  0, 0, 0],
    [0, 0.04, 0,  0, 0, 0],
    [0, -0.04, 0,  0, 0, 0],
    [0, 0.04, 0,  0, 0, 0],
    ]

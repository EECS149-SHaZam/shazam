import time
#State Constants
YAW_TRACK = 1
YAW_STAY = 2
PITCH_TRACK = 3
PITCH_STAY = 4

pitch_state = 0
yaw_state = 0
threshold = 0


#Read HID data from WiiMote. Returns a dictionary with 
def getData():
    pass

#Initial Calibration Method
def calibrate():
    pass

#Perform state transitions and logic
def stateChart():
    results = get_data()

    #State transition logic
    if results[yawAngle] >= threshold:
        yaw_state = YAW_TRACK
    elif results[yawAngle] < threshold:
        yaw_state = YAW_STAY
    if results[pitchAngle] >= threshold:
        pitch_state = PITCH_TRACK
    elif results[pitchAngle] < threshold:
        pitch_state = PITCH_STAY

    #State Action logic
    if yaw_state == YAW_STAY:
        pass
    elif yaw_state == YAW_TRACK:
        pass
    if pitch_state == PITCH_STAY:
        pass
    elif pitch_state == PITCH_TRACK;
        pass



calibrate()
while True:
    stateChart()
    time.sleep(.01)

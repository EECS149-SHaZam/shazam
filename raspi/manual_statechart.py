from statechart_class import Statechart


class ManualStatechart(Statechart):
    def __init__(self, inputs):
        super(ManualStatechart, self).__init__()
        self.inputs = inputs
        self.state = self.State()
        
    
"""
Manual mode state logic
"""
def manual_statechart():
    global MANUAL_STATE
    print "latest button is %d" %latestButton
    desiredPitch, desiredYaw = lamp['pitch'], lamp['yaw']
    if latestButton == 0:
        MANUAL_STATE = MANUAL_OFF
    if latestButton & BTN_UP:
        print("Button Up!")
        desiredPitch = lamp['pitch'] + PITCH_INC
##        if desiredPitch > mc.PITCH_UPPER_LIMIT or desiredPitch < mc.PITCH_LOWER_LIMIT:
##            MANUAL_STATE = MANUAL_RUMBLE
##        else:
        MANUAL_STATE = MANUAL_ON
    if latestButton & BTN_DOWN:
        print("Button Down!")
        desiredPitch = lamp['pitch'] - PITCH_INC
##        if desiredPitch > mc.PITCH_UPPER_LIMIT or desiredPitch < mc.PITCH_LOWER_LIMIT:
##            MANUAL_STATE = MANUAL_RUMBLE
##        else:
        MANUAL_STATE = MANUAL_ON
    if latestButton & BTN_LEFT:
        print("Button Left!")
        desiredYaw = lamp['yaw'] - YAW_INC
##        if desiredYaw > mc.YAW_UPPER_LIMIT or desiredYaw < mc.YAW_LOWER_LIMIT:
##            MANUAL_STATE = MANUAL_RUMBLE
##        else:
        MANUAL_STATE = MANUAL_ON
    if latestButton & BTN_RIGHT:
        print("Button Right!")
        desiredYaw = lamp['yaw'] + YAW_INC
##        if desiredYaw > mc.YAW_UPPER_LIMIT or desiredYaw < mc.YAW_LOWER_LIMIT:
##            MANUAL_STATE = MANUAL_RUMBLE
##        else:
        MANUAL_STATE = MANUAL_ON
    print "pitch %d yaw %d" %(desiredPitch, desiredYaw)
    if MANUAL_STATE == MANUAL_OFF:
        pass
    elif (desiredYaw > mc.YAW_UPPER_LIMIT or desiredYaw < mc.YAW_LOWER_LIMIT or
        desiredPitch > mc.PITCH_UPPER_LIMIT or desiredPitch < mc.PITCH_LOWER_LIMIT):
        MANUAL_STATE = MANUAL_RUMBLE
    else:
        MANUAL_STATE = MANUAL_ON
        
    if MANUAL_STATE == MANUAL_RUMBLE:
        wiimote.rumble = True
        return
    elif MANUAL_STATE == MANUAL_OFF:
        wiimote.rumble = False
    elif MANUAL_STATE == MANUAL_ON:
        wiimote.rumble = False
        setPitch(desiredPitch)
        setYaw(desiredYaw)
        
        print("desired pitch: %f") %(desiredPitch*rad2deg)
        print("desired yaw: %f") %(desiredYaw*rad2deg)       
        

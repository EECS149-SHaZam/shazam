import math
from statechart_class import Statechart, Messages
from rs485 import MotorController
from wiimote import connect, Lights, Buttons
import cwiid
import ir

"""
Config
"""
#State Constants
YAW_TRACK = 1
YAW_STAY = 2
PITCH_TRACK = 3
PITCH_STAY = 4

AUTO_STATE = 1
MANUAL_STATE = 2


pitch_state = PITCH_STAY
yaw_state = YAW_STAY


class MainStatechart(Statechart):
    def __init__(self, wiimote, motor_controller, *args, **kwargs):
        super(MainStatechart, self).__init__(*args, **kwargs)
        
        self.wiimote = wiimote
        self.motor_controller = motor_controller
        
        wiimote.enable(cwiid.FLAG_MESG_IFC)
        wiimote.rpt_mode = cwiid.RPT_IR | cwiid.RPT_BTN
        wiimote.mesg_callback = self.wiimote_callback
        
        self.inputs.buttons = Buttons(wiimote)
        self.inputs.points = []
        self.inputs.messages = Messages()  # Wiimote messages
        self.inputs.distances = {}
        
        self.state.auto = True
        self.state.pitch = 0
        self.state.yaw = 0
        self.state.user = {'x' : 0, 'y': 0, 'z': 0, 'roll': 0, 'pitch': 0, 'yaw': 0}
        self.state.wii = {'x' : 0, 'y': 0, 'z': 1, 'roll': 0, 'pitch': 0, 'yaw': 0}
        self.state.lamp = {'x' : 1, 'y': 0, 'z': 1, 'roll': 0, 'pitch': 0, 'yaw': 0}
    
    def __del__(self):
        self.wiimote.close()
        del self.motor_controller
        
        super(MainStatechart, self).__del__()
    
    def wiimote_callback(self, messages, time):
        self.inputs.messages.append(messages)
        self.inputs.buttons = Buttons(self.wiimote)

    def iteration_starting(self):
        if not self.state.auto:
            print "Manual mode enabled"
            return None
        else:
            print "Auto mode engaged"
        
    def read_inputs(self):
        """
        Collect data from the sensors for processing.
        """
        message = wiimote.get_mesg()
        self.inputs.messages.append(message)
        ir.update_inputs(self.inputs)
        ir.update_state(self.inputs, self.state)
        
    def update_state(self):
        """
        Using self.inputs, write the values needed to make decisions to self.state.
        """
        def calculate_CommandedPitchandYaw():
            """
            Calculate desired pitch and yaw based off of user and lamp data
            """
            # Spot offset from user
            rOff = user['z']/math.tan(user['pitch']) * (-1)
            xOff = rOff * math.cos(user['yaw']) * (-1)
            yOff = rOff * math.sin(user['yaw'])

            #Spot position in Global frame
            xSpot = user['x'] + xOff
            ySpot = user['y'] + yOff

            #Spot offset from Lamp
            xOffL = xSpot - lamp['x']
            yOffL = ySpot - lamp['y']
            rOffL = math.sqrt(xOffL*xOffL + yOffL*yOffL)

            #Lamp Pitch and Yaw commands
            lampPitch = math.atan2(lamp['z'], rOffL)
            lampYaw = math.atan2(yOffL, xOffL)

            print('xSpot - %f, ySpot - %f, lampPitch - %f, lampYaw - %f' % 
                    (xSpot, ySpot, lampPitch*(180/math.pi), lampYaw*(180/math.pi))
            )
            return lampPitch, lampYaw
        
        if self.inputs.points:
            points = self.inputs.points
        
        if self.inputs.buttons.a:
            self.state.auto = False
        if self.inputs.buttons.a and self.inputs.buttons.b:
            self.state.auto = True
        
    def perform_actions(self):
        if self.state.auto:
            Lights(self.wiimote).auto()
        else:
            Lights(self.wiimote).manual();
        

def stateChart():
    """
    Performs state transitions, motor control
    """
    """
    points = getData()
    #Returns sorted points list. If None, means invalid data
    if points == None:
        return

    try:
        update_userData(points)
    except:
        pass

    return
    com_pitch, com_yaw = calculate_CommandedPitchandYaw()
    pitch_diff = abs(com_pitch - lamp['pitch'])
    yaw_diff = abs(com_yaw - lamp['yaw'])

    #State transition logic
    if yaw_state == YAW_STAY:
        if yaw_diff > min_threshold_s or yaw_diff < max_threshold_s:
            yaw_state = YAW_TRACK
        else:
            yaw_state = YAW_STAY
    if yaw_state == YAW_TRACK:
        if yaw_diff > min_threshold_t or yaw_diff < max_threshold_t:
            yaw_state = YAW_TRACK
        else:
            yaw_state = YAW_STAY
    
    if pitch_state == PITCH_STAY:
        if pitch_diff > min_threshold_s or pitch_diff < max_threshold_s:
            pitch_state = PITCH_TRACK
        else:
            pitch_state = PITCH_STAY
    if pitch_state == PITCH_TRACK:
        if pitch_diff > min_threshold_t or pitch_diff < max_threshold_t:
            pitch_state = PITCH_TRACK
        else:
            pitch_state = PITCH_STAY


    #State Action logic. Command motors
    if yaw_state == YAW_STAY:
        pass
    elif yaw_state == YAW_TRACK:
        #Send commanded yaw angle
        pass
    if pitch_state == PITCH_STAY:
        pass
    elif pitch_state == PITCH_TRACK:
        #Send commanded pitch angle
        pass
    """


"""
Init
"""
wiimote = connect()
motor_controller = MotorController()
statechart = MainStatechart(wiimote, motor_controller)
statechart.run()


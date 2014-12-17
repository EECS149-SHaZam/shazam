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
        
    def update_state(self):
        """
        Using self.inputs, write the values needed to make decisions to self.state.
        """
        ir.update_state(self.inputs, self.state)
        
        if self.inputs.buttons.a:
            self.state.auto = False
        if self.inputs.buttons.a and self.inputs.buttons.b:
            self.state.auto = True
        
    def perform_actions(self):
        if self.state.auto:
            Lights(self.wiimote).auto()
        else:
            Lights(self.wiimote).manual();
        

"""
Init
"""
wiimote = connect()
motor_controller = MotorController()
statechart = MainStatechart(wiimote, motor_controller)
statechart.run()


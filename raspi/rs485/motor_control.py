import serial

class MotorController(object):
    class Address(object):
        P_ID = 3
        P_LED_CONTROL = 25
        P_PRESENT_POSITION = 36  # LSB of present position
        P_GOAL_POSITION = 30
        P_TORQUE_ENABLE = 24
        P_MOVING_SPEED = 32
        P_BAUD_RATE = 4
        P_PRESENT_VOLTAGE = 42
        P_MOVING = 46
        P_CW_ANGLE_LIMIT = 6
    
    class Packet(object):
        ID				   = 2
        LENGTH			   = 3
        INSTRUCTION		   = 4
        PARAMETER		   = 5
        DEFAULT_BAUDNUMBER = 1
    
    INST_WRITE = 3
    
    MIN_PITCH = 203
    MAX_PITCH = 828
    DOWN_PITCH = 515

    STRAIGHT_YAW = 362
    MIN_YAW = 50        # -90deg, left turn
    MAX_YAW = 664       # +90deg, right turn

    yawId = 2
    pitchId = 3
    broadcastId = 254  # Broad cast ID
    
    def __init__(self, device="/dev/ttyAMA0", baudrate=9600, timeout=3.0):
        self.port = serial.Serial(device, baudrate=baudrate, timeout=timeout)

    def send(self, id=0, inst=INST_WRITE, addr=0, values=bytearray()):
        if not isinstance(values, bytearray):
            values = bytearray(values)
        
        packet = self.build_packet(id, inst=inst, addr=addr, values=values)
        self.transmit_packet(packet)
        
    def build_packet(self, id=0, inst=INST_WRITE, addr=0, values=bytearray()):
        preamble = bytearray([0xff, 0xff, id])
        
        packet = bytearray([inst, addr]) + values
        length = len(packet) + 1  # +1 is for the id
        
        full_packet = preamble + bytearray([length]) + packet
        
        checksum = self.checksum(full_packet)
        full_packet.append(checksum)
        
        return full_packet
    
    @staticmethod
    def checksum(packet):
        checksum = 0
        for val in packet[2:]:
            checksum += val
        checksum &= 0xff
        return checksum
    
    def transmit_packet(self, packet):
        self.port.write(packet)
        
if __name__ == "__main__":
    mc = MotorController()
    mc.send(mc.pitchId, mc.INST_WRITE, mc.Address.P_LED_CONTROL, [1])

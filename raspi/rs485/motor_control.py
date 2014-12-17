import serial
import math
from RPi import GPIO
import time
import datetime
import sys

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
    
    MIN_PITCH = 203  # Corresponds to 0 rad
    MAX_PITCH = 828  # Corresponds to -PI rad
    DOWN_PITCH = 515
    SF_PITCH = (MAX_PITCH - MIN_PITCH)/math.pi # Scale factor for pitch commands

    STRAIGHT_YAW = 362
    MIN_YAW = 50        # +90deg, left turn
    MAX_YAW = 664       # -90deg, right turn
    SF_YAW = (MAX_YAW - MIN_YAW)/math.pi # Scale factor for yaw commands

    MAX_MOVING_SPEED = 200
    MOVING_SF = 0.111*2*math.pi/60 #0.111rpm * 2pi = 0.6974rad/min = 0.0116 rad/s (per count)
    MOVING_SF = 1/MOVING_SF # 86.0297 counts per rad/s

    # Handy Constants
    rad2deg = 180/math.pi
    deg2rad = 1/rad2deg

    @classmethod
    def calculatePitchAndYawCommand(cls, pitchRad, yawRad):
        if pitchRad < -math.pi:
            pitch = -math.pi
        elif pitchRad > 0:
            pitch = 0
        if yawRad < -math.pi:
            yawRad = -math.pi
        elif yawRad > math.pi:
            yawRad = math.pi

        pitchCommand = cls.MIN_PITCH - pitchRad*cls.SF_PITCH
        yawCommand = cls.STRAIGHT_YAW - yawRad*cls.SF_YAW

        return int(pitchCommand), int(yawCommand)
    

    yawId = 2
    pitchId = 3
    broadcastId = 254  # Broad cast ID
    
    def __init__(self, device="/dev/ttyAMA0", baudrate=57600, timeout=3.0):
        self.port = serial.Serial(device, baudrate=baudrate, timeout=timeout)
        
    def send(self, id=0, inst=INST_WRITE, addr=0, values=bytearray()):
        if not isinstance(values, bytearray):
            values = bytearray(values)
        
        packet = self.build_packet(id, inst=inst, addr=addr, values=values)
        self.transmit_packet(packet)
        
    def build_packet(self, id=0, inst=INST_WRITE, addr=0, values=bytearray()):
        if not isinstance(values, bytearray):
            values = bytearray(values)
        
        preamble = bytearray([0xff, 0xff, id])
        
        packet = bytearray([inst, addr]) + values
        length = len(packet) + 1  # +1 is for the id
        
        full_packet = preamble + bytearray([length]) + packet
        
        checksum = self.checksum(full_packet)
        full_packet.append(checksum)
        
        #self.print_packet(full_packet)
        return full_packet
    
    def pitch_to(self, pitch):
        """Set the goal pitch."""
        return self.send(
                id=self.pitchId,
                inst=self.INST_WRITE,
                addr=self.Address.P_GOAL_POSITION,
                values=self.split_int(pitch)
        )
    
    def yaw_to(self, yaw):
        """Set the goal yaw."""
        return self.send(
                id=self.yawId,
                inst=self.INST_WRITE,
                addr=self.Address.P_GOAL_POSITION,
                values=self.split_int(yaw)
        )
    
    def broadcast_rate(self, rate):
        """Set the movement rate for all motors."""
        return self.send(
                id=self.broadcastId,
                inst=self.INST_WRITE,
                addr=self.Address.P_MOVING_SPEED,
                values=self.split_int(rate)
        )
        
    def pitch_rate(self, rate):
        """Set the movement rate for pitch motor."""
        return self.send(
                id=self.pitchId,
                inst=self.INST_WRITE,
                addr=self.Address.P_MOVING_SPEED,
                values=self.split_int(rate)
        )
        
    def yaw_rate(self, rate):
        """Set the movement rate for yaw motor."""
        return self.send(
                id=self.yawId,
                inst=self.INST_WRITE,
                addr=self.Address.P_MOVING_SPEED,
                values=self.split_int(rate)
        )
        
    @staticmethod
    def checksum(packet):
        checksum = 0
        for val in packet[2:]:
            checksum += val
        checksum = ~checksum
        checksum &= 0xff
        return checksum
    
    def print_packet(self, packet):
        for i, val in enumerate(packet):
            print("%01d:  %02x (%d)" % (i, val, val))
        print("Sent")
    
    def transmit_packet(self, packet):
        #to_send = bytearray(reversed(packet))
        self.port.write(packet)
        time.sleep(0.01)
    
    def split_int(self, i):
        hi = 0xff00 & i
        hi >>= 8
        lo = 0xff & i
        return [lo, hi]
        
def enable_rts(verbose=True):
    if verbose: print("Enabling RS-485 RTS...")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)
    GPIO.output(11,True)
    if verbose: print("RTS enabled!")

def disable_rts(verbose=True):
    if verbose: print("Disabling RS-485 RTS...")
    GPIO.output(11, False)
    if verbose: print("RTS disabled")
    
    
if __name__ == "__main__":
    if '--rts' in sys.argv:
        enable_rts()
        time.sleep(1)

    mc = MotorController()
    mc.send(id=mc.broadcastId, inst=mc.INST_WRITE, addr=mc.Address.P_MOVING_SPEED, values=mc.split_int(mc.MAX_MOVING_SPEED))
    #mc.send(id=mc.pitchId, inst=mc.INST_WRITE, addr=mc.Address.P_GOAL_POSITION, values=mc.split_int(mc.MAX_PITCH))
    #mc.send(id=mc.yawId, inst=mc.INST_WRITE, addr=mc.Address.P_GOAL_POSITION, values=mc.split_int(mc.STRAIGHT_YAW))

    desiredPitch = -45*mc.deg2rad
    desiredYaw = -45*mc.deg2rad

    pitchCommand, yawCommand = mc.calculatePitchAndYawCommand(desiredPitch, desiredYaw)
    pitchCommand, yawCommand= int(pitchCommand), int(yawCommand)

    # Send commands
    mc.send(id=mc.pitchId, inst=mc.INST_WRITE, addr=mc.Address.P_GOAL_POSITION, values=mc.split_int(mc.MIN_PITCH))
    mc.send(id=mc.yawId, inst=mc.INST_WRITE, addr=mc.Address.P_GOAL_POSITION, values=mc.split_int(mc.STRAIGHT_YAW))

    abc = datetime.datetime.now().time()
    abc = time.time()
    abcf = float(abc)
    print("Time Stamp: "+str(abc))
    print("    float: %f") %(abcf)
    period = 1; #seconds
    startTime = time.time() #seconds
    sampleTime = 0.2 #0.25 #seconds
    currentPitch, currentYaw = 0, 0
    posNeg = 1
    posNegP = 1;
    while True:
        deltaTime = time.time()-startTime #seconds

        desiredYaw = posNeg*(90 * (((deltaTime % period)/period) - 0.5))
        desiredPitch = posNegP*(45 * (((deltaTime % period)/period) - 0.5))

        
        desiredPitch, desiredYaw = desiredPitch*mc.deg2rad, desiredYaw*mc.deg2rad
        if currentYaw*posNeg > 0 and desiredYaw*posNeg < currentYaw*posNeg:
            posNeg = -1 * posNeg
            desiredYaw = -1 * desiredYaw

        if currentPitch*posNegP > 0 and desiredPitch*posNegP < currentPitch*posNegP:
            posNegP = -1 * posNegP
            desiredPitch = -1 * desiredPitch

        desiredPitch = desiredPitch-(45/2)*mc.deg2rad

        print("desiredPitch: %f, posNegP: %d") %(desiredPitch*mc.rad2deg, posNegP)

        pitchRate = int(math.ceil(abs(mc.MOVING_SF*((desiredPitch - (currentPitch-(45/2)*mc.deg2rad))/sampleTime))))
        yawRate = int(math.ceil(abs(mc.MOVING_SF*((desiredYaw - currentYaw)/sampleTime))))
        #mc.send(id=mc.pitchId, inst=mc.INST_WRITE, addr=mc.Address.P_MOVING_SPEED, values=mc.split_int(pitchRate))
        #mc.send(id=mc.yawId, inst=mc.INST_WRITE, addr=mc.Address.P_MOVING_SPEED, values=mc.split_int(yawRate))
        mc.pitch_rate(pitchRate)
        mc.yaw_rate(yawRate)
        
        pitchCommand, yawCommand = mc.calculatePitchAndYawCommand(desiredPitch,desiredYaw)
        print("yawRate: %d") %(yawRate)
        #mc.send(id=mc.pitchId, inst=mc.INST_WRITE, addr=mc.Address.P_GOAL_POSITION, values=mc.split_int(pitchCommand))
        #mc.send(id=mc.yawId, inst=mc.INST_WRITE, addr=mc.Address.P_GOAL_POSITION, values=mc.split_int(yawCommand))
        mc.pitch_to(pitchCommand)
        mc.yaw_to(yawCommand)

        currentPitch, currentYaw = desiredPitch+(45/2)*mc.deg2rad, desiredYaw
        
        time.sleep(sampleTime)
        
        
        

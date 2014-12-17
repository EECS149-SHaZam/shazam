from __future__ import division
import time, math
import cwiid
from wiimote import connect, Lights
from rs485 import motor_control

"""
Read HID data from WiiMote and return list points of infrared positions
"""
def getData():
    if not AUTO_MODE:
        if verbose:
            print "Manual mode enabeled"
        manual_statechart()
        return None
    else:
        if verbose:
            print "Auto mode engaged"
    temp_points = [] #Unordered point data
    point1, point2, point3, point4 = 0, 0, 0, 0
    #Grab relevant data from Wii and put in temp_points
    messages = latestMessages

    if not (type(messages[0][1]) is list) or  None in messages[0][1]:
        return None
    for msg in messages[0][1]:   # Loop through IR LED sources
        temp_points.append(msg['pos'])
                         
    if len(temp_points) != 4:
        if verbose:
            print ('Invalid temp point length %d' %temp_points)
        return None

    #print messages
                             
    #Calculate respective distances for all pairs of points and put in distances dictionary
    getDistances(temp_points)
    #Indices of min pair of points
    indexA, indexB = min(distances, key=distances.get)
    #Find point1 and point2 based on indexA and indexB
    point1, point2, point3, point4 = findPoints(temp_points, indexA, indexB)

    return [temp_points[point1], temp_points[point2], temp_points[point3], temp_points[point4]]

"""
Manual mode state logic
"""
def manual_statechart():
    global MANUAL_STATE
    if verbose:
        print "latest button is %d" %latestButton
    desiredPitch, desiredYaw = lamp['pitch'], lamp['yaw']
    if latestButton == 0:
        MANUAL_STATE = MANUAL_OFF
    if latestButton & BTN_UP:
        if verbose:
            print("Button Up!")
        desiredPitch = lamp['pitch'] + PITCH_INC
##        if desiredPitch > mc.PITCH_UPPER_LIMIT or desiredPitch < mc.PITCH_LOWER_LIMIT:
##            MANUAL_STATE = MANUAL_RUMBLE
##        else:
        MANUAL_STATE = MANUAL_ON
    if latestButton & BTN_DOWN:
        if verbose:
            print("Button Down!")
        desiredPitch = lamp['pitch'] - PITCH_INC
##        if desiredPitch > mc.PITCH_UPPER_LIMIT or desiredPitch < mc.PITCH_LOWER_LIMIT:
##            MANUAL_STATE = MANUAL_RUMBLE
##        else:
        MANUAL_STATE = MANUAL_ON
    if latestButton & BTN_LEFT:
        if verbose:
            print("Button Left!")
        desiredYaw = lamp['yaw'] - YAW_INC
##        if desiredYaw > mc.YAW_UPPER_LIMIT or desiredYaw < mc.YAW_LOWER_LIMIT:
##            MANUAL_STATE = MANUAL_RUMBLE
##        else:
        MANUAL_STATE = MANUAL_ON
    if latestButton & BTN_RIGHT:
        if verbose:
            print("Button Right!")
        desiredYaw = lamp['yaw'] + YAW_INC
##        if desiredYaw > mc.YAW_UPPER_LIMIT or desiredYaw < mc.YAW_LOWER_LIMIT:
##            MANUAL_STATE = MANUAL_RUMBLE
##        else:
        MANUAL_STATE = MANUAL_ON
    if verbose:
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
        
        if verbose:
            print("desired pitch: %f") %(desiredPitch*rad2deg)
            print("desired yaw: %f") %(desiredYaw*rad2deg)       
        
    
"""
Calculate all distances of points in list points and returns dictionary of form
    {(pointA, pointB): distance}
"""
def getDistances(points):
    for i in range(0, len(points)):
        for j in range(0, len(points)):
            if i != j:
                distances[(i, j)] = compute_distance(points[i], points[j])
            else:
                distances[(i, j)] = float('inf')
"""
Given temp_points, and indexA and indexB, find 
point1, point2, point3, and point4
"""

def findPoints(temp_points, indexA, indexB):
    point1, point2, point3, point4 = 0, 0, 0, 0
    indexC = 0
    for i in range(0, len(temp_points)):
        if i != indexA and i!= indexB:
            indexC = i
            break
    
    distanceA = distances[(indexA, indexC)]
    distanceB = distances[(indexB, indexC)]
    if distanceA > distanceB:
        point1 = indexA
        point2 = indexB
    else:
        point1 = indexB
        point2 = indexA

    #Find point3 and point4 based on indexC and indexD
    indexD = 6 - (indexA + indexB + indexC)
    if temp_points[indexC][1] <= temp_points[indexD][1]:
        point3 = indexC
        point4 = indexD
    else:
        point3 = indexD
        point4 = indexC
    return point1, point2, point3, point4


"""
Populates user dictionary with user's x, y, z position
and pitch and roll
"""
def update_userData(points):
    psi1, psi2, psi3 = points[0][0], points[1][0], points[2][0]
    theta3, theta4 = points[2][1], points[3][1]

    #Convert from camera pixels to radians
    psi1 = (psi1-xPixOffset)*radPerPix
    psi2 = (psi2-xPixOffset)*radPerPix
    psi3 = (psi3-xPixOffset)*radPerPix

    theta3 = (theta3-yPixOffset)*radPerPix
    theta4 = (theta4-yPixOffset)*radPerPix
    #print "psi1: %f psi2: %f psi3:%f" %(psi1*rad2deg, psi2*rad2deg, psi3*rad2deg)
    #print "theta3: %f theta4: %f" %(theta3*rad2deg, theta4*rad2deg)
    
    c = (l_23/l) * (math.tan(psi1)-math.tan(psi3))/(math.tan(psi2)-math.tan(psi3))
    a = 1-c #1 - c
    b = math.tan(psi1) - (math.tan(psi2) * c)

    psi_u = math.atan2(-a, b)
    #print "psi1: %f psi2: %f psi3: %f psi_u: %f c: %f" %(psi1*rad2deg, psi2*rad2deg, psi3*rad2deg, psi_u*rad2deg, c)

    x3 = l*(math.cos(psi_u) + math.sin(psi_u)*math.tan(psi1))/(math.tan(psi1)-math.tan(psi3))
    y3 = x3*(math.tan(psi3) * (-1))
    z3 = x3*math.tan(theta3)
    
    x_u = x3 - ((l/2)*math.sin(psi_u))
    y_u = y3 - ((l/2)*math.cos(psi_u))
    z_u = z3
    
    #x_u = (l * (math.cos(psi_u) + math.sin(psi_u) * (math.tan(psi1) - .5)))/(math.tan(psi1) - math.tan(psi3))
    #y_u = x_u * math.tan(psi_u)
    #z_u = (x_u + l/2 * math.sin(psi_u)) * math.tan(theta3)

    #z3 = z_u
    #x3 = (x_u + l/2 * math.sin(psi_u))
    r3 = math.sqrt(x3*x3 + z3*z3)
    #print "z_u: %f x_u: %f y_u: %f psi_u: %f" %(z_u, x_u, y_u, psi_u*rad2deg)
    theta_prime = abs(theta4-theta3)
    h_prime = r3 * math.sin(theta_prime)
    alpha = math.pi/2 - theta3
    beta = math.pi/2 - theta_prime
    #print "h_prime: %f" %h_prime
    if h_prime > h:
        h_prime = h
    gamma = math.acos(h_prime/h)
    theta_u = -math.pi + alpha + beta - gamma
    if theta_u > 0:
        thetau = -math.pi + alpha + beta + gamma

    #print "theta_u: %f psi_u %f" %(theta_u*rad2deg, psi_u*rad2deg)

    user['x'], user['y'], user['z'] = x_u, y_u, z_u
    user['yaw'], user['pitch'] = psi_u, theta_u


"""
Calculate desired pitch and yaw based off of user and lamp data
"""
def calculate_CommandedPitchandYaw():
##    # Spot offset from user
##    rOff = user['z']/math.tan(user['pitch']) * (-1)
##    xOff = rOff * math.cos(user['yaw']) * (-1)
##    yOff = rOff * math.sin(user['yaw'])
##
##    #Spot position in Global frame
##    xSpot = user['x'] + xOff
##    ySpot = user['y'] + yOff
##
##    #Spot offset from Lamp
##    xOffL = xSpot - lamp['x']
##    yOffL = ySpot - lamp['y']
##    rOffL = math.sqrt(xOffL*xOffL + yOffL*yOffL)
##
##    #Lamp Pitch and Yaw commands
##    lampPitch = math.atan2(lamp['z'], rOffL)
##    lampYaw = math.atan2(yOffL, xOffL)
    
    #User offset from Lamp
    xOffL = user['x'] - lamp['x']
    yOffL = user['y'] - lamp['y']
    zOffL = user['z'] - lamp['z'] # add 20cm to avoid user's eyes
    rOffL = math.sqrt(xOffL*xOffL + yOffL*yOffL)

    #Lamp Pitch and Yaw commands
    lampPitch = math.atan2(zOffL, rOffL)
    lampYaw = math.atan2(yOffL, xOffL)

    #print ('xOffL - %f, yOffL - %f, lampPitch - %f, lampYaw - %f' %(xOffL, yOffL, lampPitch*rad2deg, lampYaw*rad2deg))
    if verbose:
        print "lampPitch: %f, lampYaw: %f" %(lampPitch*rad2deg, lampYaw*rad2deg)
    return lampPitch, lampYaw

"""
Set lamp Pitch through the motor controller
"""
def setPitch(desiredPitch):
    pitchLimited, pitchCommand = mc.calculatePitchCommand(desiredPitch)
    pitchRate = int(math.ceil(abs(mc.MOVING_SF*((pitchLimited - lamp['pitch'])/SAMPLE_TIME))))

    # Protect against pitchRate = 0 giving max rate
    if pitchRate == 0:
        pitchRate = 100

    mc.pitch_rate(pitchRate)
    mc.pitch_to(pitchCommand)

    lamp['pitch'] = pitchLimited
    if verbose:
        print "pitchLimited %f" %(pitchLimited*rad2deg)

"""
Set lamp Yaw through the motor controller
"""
def setYaw(desiredYaw):
    yawLimited, yawCommand = mc.calculateYawCommand(desiredYaw)
    yawRate = int(math.ceil(abs(mc.MOVING_SF*((yawLimited - lamp['yaw'])/SAMPLE_TIME))))

    # Protect against yawRate = 0 giving max rate
    if yawRate == 0:
        yawRate = 100
    
    mc.yaw_rate(yawRate)
    mc.yaw_to(yawCommand)

    lamp['yaw'] = yawLimited
    if verbose:
        print "yawLimited %f" %(yawLimited*rad2deg)

"""
Compute distances between p1, p2 using distance formula
"""
def compute_distance(p1, p2):
    x = p1[0]-p2[0]
    y = p1[1]-p2[1]
    return math.sqrt(math.pow(x, 2) + math.pow(y, 2))

"""
Zero Out Motors
"""
def calibrate():
    pass

"""
Performs state transitions, motor control
"""
def stateChart():
    global yaw_state
    global pitch_state
    points = getData()
    #Returns sorted points list. If None, means invalid data or running in manual mode
    if points == None:
        return
    try:
        update_userData(points)
    except:
        pass

    #return
    com_pitch, com_yaw = calculate_CommandedPitchandYaw()
    pitch_diff = abs(com_pitch - lamp['pitch'])
    yaw_diff = abs(com_yaw - lamp['yaw'])

    #State transition logic
    if yaw_state == YAW_STAY:
        if yaw_diff > min_threshold_s and yaw_diff < max_threshold_s:
            yaw_state = YAW_TRACK
        else:
            yaw_state = YAW_STAY
    if yaw_state == YAW_TRACK:
        if yaw_diff > min_threshold_t and yaw_diff < max_threshold_t:
            yaw_state = YAW_TRACK
        else:
            yaw_state = YAW_STAY
    
    if pitch_state == PITCH_STAY:
        if pitch_diff > min_threshold_s and pitch_diff < max_threshold_s:
            pitch_state = PITCH_TRACK
        else:
            pitch_state = PITCH_STAY
    if pitch_state == PITCH_TRACK:
        if pitch_diff > min_threshold_t and pitch_diff < max_threshold_t:
            pitch_state = PITCH_TRACK
        else:
            pitch_state = PITCH_STAY


    #State Action logic. Command motors
    if yaw_state == YAW_STAY:
        pass
    elif yaw_state == YAW_TRACK:
        #Send commanded yaw angle
        setYaw(com_yaw)
    if pitch_state == PITCH_STAY:
        pass
    elif pitch_state == PITCH_TRACK:
        #Send commanded pitch angle
        setPitch(com_pitch)

def callback_function(messages, time):
    global latestMessages
    global AUTO_MODE
    global latestButton
    latestMessages = messages
    latestButton = wiimote.state['buttons']
    if latestButton == cwiid.BTN_A:
        AUTO_MODE = False
        wiimote.led = 2 | 4
    if latestButton == cwiid.BTN_A + cwiid.BTN_B:
        AUTO_MODE = True
        wiimote.led = 1 | 8
        setPitch(0); setYaw(0)

"""
Init
"""
#State Constants
YAW_TRACK = 1
YAW_STAY = 2
PITCH_TRACK = 3
PITCH_STAY = 4
MANUAL_OFF = 5
MANUAL_ON = 6
MANUAL_RUMBLE = 7
MANUAL_STATE = MANUAL_OFF
BTN_UP = 2048
BTN_DOWN = 1024
BTN_LEFT = 256
BTN_RIGHT = 512

SAMPLE_TIME = 0.2
#Manual Control Constants
PITCH_INC = math.pi/4 * SAMPLE_TIME
YAW_INC = math.pi/4 * SAMPLE_TIME


#LED Configuration Params
l_12 = 0.064
l_23 = 0.133
l = l_12 + l_23
h = 0.171

#Wiimote Camera Params
rad2deg = 180/math.pi
deg2rad = 1/rad2deg
radPerPix = 0.197/250 #(40*deg2rad)/1024.0
xPixOffset = 1024/2
yPixOffset = 768/2

pitch_state = PITCH_STAY
yaw_state = YAW_STAY
max_threshold_s = 25*math.pi/180
min_threshold_s = 0# 1*math.pi/180
max_threshold_t = max_threshold_s * .5
min_threshold_t = min_threshold_s * .5

user = {'x' : 0, 'y': 0, 'z': 0, 'roll': 0, 'pitch': 0, 'yaw': 0}
wii = {'x' : 0, 'y': 0, 'z': 0, 'roll': 0, 'pitch': 0, 'yaw': 0}
lamp = {'x' : .013, 'y': -.17, 'z': -0.056, 'roll': 0, 'pitch': 0, 'yaw': 0}

distances = {}
AUTO_MODE = True

    
def run():
    global latestMessages
    global latestButton
    
    setPitch(lamp['pitch']); setYaw(lamp['yaw'])
    """
    Main execution block
    """
    wiimote.enable(cwiid.FLAG_MESG_IFC)
    wiimote.rpt_mode = cwiid.RPT_IR | cwiid.RPT_BTN
    wiimote.mesg_callback = callback_function
    wiimote.led = 1 | 8
    latestMessages = wiimote.get_mesg()
    latestButton = 0
    calibrate()
    while True:
        stateChart()
        time.sleep(SAMPLE_TIME)

def deploy(wm, motor_controller):
    global wiimote
    global mc
    wiimote = wm
    mc = motor_controller
    run()

verbose = False
if __name__ == "__main__":
    verbose = True
    mc = motor_control.MotorController()
    if verbose:
        print("Pairing..")
    wiimote = cwiid.Wiimote()
    if verbose:
        print("Paired")
    deploy(mc, wiimote)

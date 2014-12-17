import math
import config as cfg

#Wiimote Camera Params
rad2deg = 180/math.pi
deg2rad = 1/rad2deg


def update_inputs(inputs):
    """
    Get IR point data from the wiimote's camera message
    """
    message = inputs.messages[-1]  # last message
    
    temp_points = []  # Unordered point data
    point1, point2, point3, point4 = 0, 0, 0, 0
    #Grab relevant data from Wii and put in temp_points
    print message
    if not (type(message[0][1]) is list) or None in message[0][1]:
        return None
    for msg in message[0][1]:   # Loop through IR LED sources
        temp_points.append(msg['pos'])
                         
    if len(temp_points) != 4:
        print ('Invalid temp point length %d' %temp_points)
        return None

    print message
                             
    #Calculate respective distances for all pairs of points and put in distances dictionary
    distances = getDistances(temp_points)
    inputs.distances = distances
    #Indices of min pair of points
    indexA, indexB = min(distances, key=distances.get)
    #Find point1 and point2 based on indexA and indexB
    point1, point2, point3, point4 = findPoints(temp_points, indexA, indexB, distances)
    
    inputs.points = [temp_points[point1], temp_points[point2], temp_points[point3], temp_points[point4]]

def findPoints(temp_points, indexA, indexB, distances):
    """
    Given temp_points, and indexA and indexB, find 
    point1, point2, point3, and point4
    """
    point1, point2, point3, point4 = 0, 0, 0, 0
    indexC = 0
    for i in range(0, len(temp_points)):
        if i != indexA and i != indexB:
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

def getDistances(points):
    """
    Calculate all distances of points in list points and returns dictionary of form
        {(pointA, pointB): distance}
    """
    distances = {}
    for i, point_i in enumerate(points):
        for j, point_j in enumerate(points):
            if i != j:
                distances[(i, j)] = compute_distance(point_i, point_j)
            else:
                distances[(i, j)] = float('inf')
    return distances
                
def compute_distance(p1, p2):
    """
    Compute distances between p1, p2 using distance formula
    """
    x = p1[0]-p2[0]
    y = p1[1]-p2[1]
    return math.sqrt(math.pow(x, 2) + math.pow(y, 2))


def update_state(inputs, state):
    """
    Populates user dictionary with user's x, y, z position
    and pitch and roll
    """
    points = inputs.points
    if not points:
        return
    psi1, psi2, psi3 = points[0][0], points[1][0], points[2][0]
    theta3, theta4 = points[2][1], points[3][1]

    #Convert from camera pixels to radians
    psi1 = (psi1 - cfg.xPixOffset)*cfg.radPerPix
    psi2 = (psi2 - cfg.xPixOffset)*cfg.radPerPix
    psi3 = (psi3 - cfg.xPixOffset)*cfg.radPerPix

    theta3 = (theta3 - cfg.yPixOffset)*cfg.radPerPix
    theta4 = (theta4 - cfg.yPixOffset)*cfg.radPerPix
    #print "psi1: %f psi2: %f psi3:%f" %(psi1*rad2deg, psi2*rad2deg, psi3*rad2deg)
    #print "theta3: %f theta4: %f" %(theta3*rad2deg, theta4*rad2deg)
    
    c = (cfg.l_23/cfg.l) * (math.tan(psi1)-math.tan(psi3))/(math.tan(psi2)-math.tan(psi3))
    a = 1-c #1 - c
    b = math.tan(psi1) - (math.tan(psi2) * c)

    psi_u = math.atan2(-a, b)
    print "psi1: %f psi2: %f psi3: %f psi_u: %f c: %f" %(psi1*rad2deg, psi2*rad2deg, psi3*rad2deg, psi_u*rad2deg, c)

    x3 = cfg.l*(math.cos(psi_u) + math.sin(psi_u)*math.tan(psi1))/(math.tan(psi1)-math.tan(psi3))
    y3 = x3*(math.tan(psi3) * (-1))
    z3 = x3*math.tan(theta3)
    
    x_u = x3 - ((cfg.l/2)*math.sin(psi_u))
    y_u = y3 - ((cfg.l/2)*math.cos(psi_u))
    z_u = z3
    
    #x_u = (cfg.l * (math.cos(psi_u) + math.sin(psi_u) * (math.tan(psi1) - .5)))/(math.tan(psi1) - math.tan(psi3))
    #y_u = x_u * math.tan(psi_u)
    #z_u = (x_u + cfg.l/2 * math.sin(psi_u)) * math.tan(theta3)

    #z3 = z_u
    #x3 = (x_u + cfg.l/2 * math.sin(psi_u))
    r3 = math.sqrt(x3*x3 + z3*z3)
    #print "z_u: %f x_u: %f y_u: %f psi_u: %f" %(z_u, x_u, y_u, psi_u*rad2deg)
    theta_prime = abs(theta4-theta3)
    h_prime = r3 * math.sin(theta_prime)
    alpha = math.pi/2 - theta3
    beta = math.pi/2 - theta_prime
    #print "h_prime: %f" %h_prime
    if h_prime > cfg.h:
        h_prime = cfg.h
    gamma = math.acos(h_prime/cfg.h)
    theta_u = -math.pi + alpha + beta - gamma
    if theta_u > 0:
        thetau = -math.pi + alpha + beta + gamma

    #print "theta_u: %f psi_u %f" %(theta_u*rad2deg, psi_u*rad2deg)

    user = state.user  # result
    user['x'], user['y'], user['z'] = x_u, y_u, z_u
    user['yaw'], user['pitch'] = psi_u, theta_u


import math


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

    return inputs.points

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


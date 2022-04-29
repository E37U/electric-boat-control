#E37U

from math import radians, cos, sin, asin, sqrt
import time


currentPosition = [0,0]
distanceTraveled = 0
internalSpeed = 1
lastPullTime = 0


#NOTE Since this needs to be able to run on a desktop machine, pulls to the GPIO bus and GPS are left out because the program will not run without the hardware being present
#In place of these calls, stawman calls to pointless but correctly typed data are placed so the program can run

def getPosition():
    #This function returns the current position as a tuple of latitude and longitude
    #Depending on the type of GPS used, the calls here will be VERY different but the important part is that lat and lon are  returned as decomal values
    #See note above for strawman explanation
    a = 1 #NOTE strawman, Latitude (decimal)
    b = 1 #NOTE strawman, Longitude (decimal)
    return [a,b]

def setStartPosition():
    global currentPosition
    # Pull position and initialize it
    currentPosition = getPosition()
    return

def addPositionToDistance():
    global currentPosition
    global distanceTraveled
    global internalSpeed
    global lastPullTime
    # When this is called, pull position and then calculate distance from last position, then add to total, also calculate speed
    currentTime = time.time()
    timeDiff = (currentTime - lastPullTime) /3600 # Time difference will be in hours
    distance = 0
    lastPosition = currentPosition
    currentPosition = getPosition()
    #Distance calculation from https://www.geeksforgeeks.org/program-distance-two-points-earth/#:~:text=For%20this%20divide%20the%20values,is%20the%20radius%20of%20Earth.
    radLastPosition = [radians(lastPosition[0]), radians(lastPosition[1])]
    radCurrentPosition = [radians(currentPosition[0]), radians(currentPosition[1])]

    dlon = radCurrentPosition[1] - radLastPosition[1]
    dlat = radCurrentPosition[0] - radLastPosition[0]
    a = sin(dlat / 2)**2 + cos(radLastPosition[0]) * cos(radCurrentPosition[0]) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    r = 3956
    distance = c * r
    distanceTraveled = distanceTraveled + distance
    internalSpeed = distance / timeDiff
    lastPullTime = currentTime
    return

def setThrottle(input): # convert percentage throttle to physical output
    #NOTE Strawman
    return

class dataPull():
    global internalSpeed
    global distanceTraveled
    batteryVoltage =  54.1 #NOTE Strawman
    motorCurrent  = 100.17 #NOTE Strawman
    position = getPosition()
    speed = internalSpeed
    distance = distanceTraveled
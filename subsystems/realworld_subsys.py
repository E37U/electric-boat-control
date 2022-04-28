#E37U

from math import radians, cos, sin, asin, sqrt
import time


currentPosition = [0,0]
distanceTraveled = 0
internalSpeed = 0
lastPullTime = 0

def getPosition():
    #TODO this function returns the current position as a tuple of latitude and longitude, if it can't find position, return null
    a = 1 #TODO strawman
    b = 1 #TODO strawman
    return [a,b]

def setStartPosition():
    # Pull position and initialize it
    currentPosition = getPosition()
    return

def addPositionToDistance():
    # When this is called, pull position and then calculate distance from last position, then add to total, also calculate speed
    currentTime = time.time()
    timeDiff = (currentTime - lastPullTime) /3600 # Time difference will be in hours
    distance = 0
    lastPosition = currentPosition
    currentPosition = getPosition()
    #From https://www.geeksforgeeks.org/program-distance-two-points-earth/#:~:text=For%20this%20divide%20the%20values,is%20the%20radius%20of%20Earth.
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
    #TODO either PWM or some value, idk, just set it.
    return

class dataPull(): #TODO Strawman
    batteryVoltage =  54.1 #TODO
    motorCurrent  = 100.17 #TODO
    position = getPosition()
    speed = internalSpeed
#E37U

from math import radians, cos, sin, asin, sqrt
import time

#import pynmea2 #Import for GPS
#import RPI.GPIO as GPIO #Import for raspberry pi, commented out for running on desktops

currentPosition = [0,0]
distanceTraveled = 0
internalSpeed = 1
lastPullTime = 0



def getPosition():
    #This function returns the current position as a tuple of latitude and longitude
    #Depending on the type of GPS used, the calls here will be VERY different but the important part is that lat and lon are  returned as decomal values
    #One such device is a USB Serial based NMEA GPS receiver. This uses NMEA0183 to send messages with data about position which can be called into our code with a library called pynmea2
    #We can use this library to parse messages given by the receiver, I've listed the code to do so below, note that the import is commented out in the file header because this code will only run on a raspberry pi
    #Citation for NMEA code: https://python.plainenglish.io/receiving-and-processing-gps-data-using-external-receiver-with-python-24d3592ad2e0
    ##message = open("gps_data_20220429-100657.nmea", "rb") #This file will be created by the NMEA datastream, thsi file will look like this (note the date and time) but with a path in /dev/
    ##gga = pynmea2.parse(message)
    ##a = gga.latitude  #replace strawman
    ##b = gga.longitude #replace strawman
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

#Below is the code for running the GPIO PWM output, it is commented out to run on desktops as it can only run on a raspberry pi. For integration, uncomment
#Citation: https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/
##GPIO.setmode(GPIO.BOARD)
##GPIO.setup(12, GPIO.OUT) #PWM Output
##GPIO.setup(9, GPIO.IN) #Battery Voltage In
##GPIO.setup(10, GPIO.IN) # Motor Current In
##pwm = GPIO.PWM(1, 30000) #start GPIO pin
##pwm.start(0.0) #Set to 0

def setThrottle(input): # convert percentage throttle to physical output
    ##global pwm
    ##pwm.ChangeDutyCycle(input)
    return

class dataPull():
    global internalSpeed
    global distanceTraveled
    batteryVoltage =  54.1 #NOTE Strawman
    motorCurrent  = 100.17 #NOTE Strawman
    #batteryVoltage =  GPIO.input(9) #NOTE Real code commented out while running on desktop, when running on raspberry pi, replace strawman
    #motorCurrent  = GPIO.input(10) #NOTE Real code commented out while running on desktop, when running on raspberry pi, replace strawman
    position = getPosition()
    speed = internalSpeed
    distance = distanceTraveled
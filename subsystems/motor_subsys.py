#E37U

import subsystems.realworld_subsys

import modules.configmodule

throttleValue = 0
throttleMax = float(modules.configmodule.config['Throttle']['throttle_hard_max'])
motorAmp = 0

class dataPull():
    global motorAmp
    motorCurrent = motorAmp 

def setThrottle(input):
    global throttleValue
    if input > throttleMax:
        throttleValue = throttleMax
        subsystems.realworld_subsys.setThrottle(throttleMax)
    else:
        throttleValue = input
        subsystems.realworld_subsys.setThrottle(input)
    return
def bumpThrottleDown():
    newInput = throttleValue - float(modules.configmodule.config['Throttle']['throttle_bump_margin']) #We use the margin for how big of throttle steps we use when testing if we can go faster or slower in the control loop
    if newInput < 0: #Don't let throttle go below 0, if it trues, just set it to 0
        setThrottle(0)
    else:
        setThrottle(newInput)

def bumpThrottleUp():
    newInput = throttleValue + float(modules.configmodule.config['Throttle']['throttle_bump_margin']) #We use the margin for how big of throttle steps we use when testing if we can go faster or slower in the control loop
    if newInput > throttleMax: #don't let throttle go above max
        setThrottle(throttleMax)
    else: #if it is, just use the max
        setThrottle(newInput)

def setThrottleAmp(input): #Sets the throttle from a specific amperage rather than a percent)
    global motorAmp
    if input < float(modules.configmodule.config['Throttle']['motor_amp_max']): #Testing if above max
        motorAmp = input
        setThrottle(ampToPercent(input))
    else: #if it is, just use the max
        motorAmp = float(modules.configmodule.config['Throttle']['motor_amp_max'])
        setThrottle(ampToPercent(float(modules.configmodule.config['Throttle']['motor_amp_max'])))
    return

def ampToPercent(input): # Translates amperage to percentage throttle (motor model)
    return (input /120)
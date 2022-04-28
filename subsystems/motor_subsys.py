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
    #TODO PRACTICALLY OUTPUT set throttle to said input
    if input > throttleMax:
        throttleValue = throttleMax
        subsystems.realworld_subsys.setThrottle(throttleMax)
    else:
        throttleValue = input
        subsystems.realworld_subsys.setThrottle(input)
    return
def bumpThrottleDown():
    newInput = throttleValue - float(modules.configmodule.config['Throttle']['throttle_bump_margin'])
    setThrottle(newInput)

def bumpThrottleUp():
    newInput = throttleValue + float(modules.configmodule.config['Throttle']['throttle_bump_margin'])
    if newInput > throttleMax:
        setThrottle(throttleMax)
    else:
        setThrottle(newInput)

def setThrottleAmp(input): #Sets the throttle from a specific amperage rather than a percent)
    global motorAmp
    if input < float(modules.configmodule.config['Throttle']['motor_amp_max']):
        motorAmp = input
        setThrottle(ampToPercent(input))
    else:
        motorAmp = float(modules.configmodule.config['Throttle']['motor_amp_max'])
        setThrottle(ampToPercent(float(modules.configmodule.config['Throttle']['motor_amp_max'])))
    return

def ampToPercent(input): # Translates amperage to percentage throttle (motor model)
    return 0 #TODO implement
#E37U

import subsystems.error_log_subsys
import subsystems.battery_subsys
import subsystems.solar_subsys
import subsystems.realworld_subsys
import subsystems.motor_subsys

import modules.configmodule

import time, datetime

#Examples of how to pull params
#modules.configmodule.config.read('config.ini')
#print(modules.configmodule.config.sections())
#print('bit' in modules.configmodule.config.sections())
#print(modules.configmodule.config['Race']['race_length'])

class dataHolding():
    time = 0
    class real():
        batteryVoltage = 0
        motorCurrent  = 0
        position = [0,0]
    
    class model():
        batterySOC = 1
        motorCurrent  = 0
    # How you can work with data: dataHolding.real.batteryVoltage = 10

def mainControlLoop():
    freezeData = dataHolding()

    # Freeze time
    freezeData.time = time.time() # this is in seconds

    # Update position and distance
    subsystems.realworld_subsys.addPositionToDistance()
    freezeData.real.position = subsystems.realworld_subsys.getPosition()

    # Pull real worlds into temp
    freezeData.real.batteryVoltage = subsystems.realworld_subsys.dataPull.batteryVoltage
    freezeData.real.motorCurrent = subsystems.realworld_subsys.dataPull.motorCurrent
    
    # Pull models into temp
    freezeData.model.batterySOC = subsystems.battery_subsys.voltageToSOC(freezeData.real.batteryVoltage)
    freezeData.model.motorCurrent = subsystems.motor_subsys.dataPull.motorCurrent
    
    # Run error/log sub system
    subsystems.error_log_subsys.errorComparator(freezeData)

    # Decide if throttle correction is required
    distanceRemaining = float(modules.configmodule.config['Race']['race_length']) - subsystems.realworld_subsys.distanceTraveled

    #Check how much harder we can push, if we can push harder, then give a bump and check results

    remainingTime = subsystems.realworld_subsys.dataPull.speed * distanceRemaining # In MPH
    ampDiff = (subsystems.battery_subsys.voltageToSOC(subsystems.realworld_subsys.dataPull.batteryVoltage) * 280/remainingTime) - subsystems.realworld_subsys.dataPull.motorCurrent #This is the value of amps we could still be pulling, this isnt an optimal value though because changing the throttle will also change speed, which is why the small changes and tests are necessary 
    if ampDiff > 5:
        subsystems.motor_subsys.bumpThrottleUp()

    #Now check current speed, if good stay, if we're too fast, drop it, if not we'll get another bump on the next loop. This keeps large fluxuations down
    remainingTime = subsystems.realworld_subsys.dataPull.speed * distanceRemaining # In MPH
    energyNeeded = remainingTime * subsystems.realworld_subsys.dataPull.motorCurrent # In Ah
    if ((subsystems.battery_subsys.voltageToSOC(subsystems.realworld_subsys.dataPull.batteryVoltage) * 280)- float(modules.configmodule.config['Battery']['battery_reserve'])) >= energyNeeded:
        return #we're satisfied so we can move on
    else: #being here means we don't have enough energy and we need to decrease speed
        satisfied = False
        while(satisfied == False):
            subsystems.motor_subsys.bumpThrottleDown()
            time.sleep(7) # wait 7 seconds for boat to settle into new throttle
            remainingTime = subsystems.realworld_subsys.dataPull.speed * distanceRemaining # In MPH
            energyNeeded = remainingTime * subsystems.realworld_subsys.dataPull.motorCurrent # In Ah
            if ((subsystems.battery_subsys.voltageToSOC(subsystems.realworld_subsys.dataPull.batteryVoltage) * 280)- float(modules.configmodule.config['Battery']['battery_reserve'])) >= energyNeeded:
                satisfied = True
            if subsystems.motor_subsys.throttleValue == 0:
                subsystems.error_log_subsys.class5Error()


## Initialization Steps

# System checks
subsystems.error_log_subsys.initialChecks()

# command line go wait

input("Press any key to start race system. NOTE: Motor will start upon trigger")

# Set full throttle
subsystems.motor_subsys.setThrottle(1.0)


#Set beginning Position
subsystems.realworld_subsys.setStartPosition()

# Loop!
while(subsystems.realworld_subsys.distanceTraveled < float(modules.configmodule.config['Race']['race_length'])):
    mainControlLoop()
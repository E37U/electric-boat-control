#E37U

import subsystems.error_log_subsys
import subsystems.battery_subsys
import subsystems.realworld_subsys
import subsystems.motor_subsys

import modules.configmodule

import time, datetime

#Examples of how to pull params
#modules.configmodule.config.read('config.ini')
#print(modules.configmodule.config.sections())
#print('bit' in modules.configmodule.config.sections())
#print(modules.configmodule.config['Race']['race_length'])

class dataHolding(): #This is an easy way to pull together all the data at once every time the main control loop runs
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

    ## Decide if throttle correction is required
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
            if subsystems.motor_subsys.throttleValue == 0: #This means we've gon to such a low throttle that we can't go any lower and still complete the race
                subsystems.error_log_subsys.class5Error()


## Initialization Steps

# System checks
subsystems.error_log_subsys.initialChecks()

# command line go wait

input("Press any key to start race system. NOTE: Motor will start upon trigger: ")

# Set full throttle
subsystems.motor_subsys.setThrottle(1.0)


#Set beginning Position
subsystems.realworld_subsys.setStartPosition()

print("Ignore message below, the model is warming up. We cannot disable the warning") #There is a warning while the model is warming up about the root finding package not iterating, once the model warms up it goes away but I can't override the message so this lets the user know everything is all good
# Run the Loop!
while(subsystems.realworld_subsys.distanceTraveled < float(modules.configmodule.config['Race']['race_length'])): #While the race isn't finished
    mainControlLoop()
    time.sleep(float(modules.configmodule.config['Loop Times']['main_loop_frequency'])) #Loop is spaced out as specified in config file
    print("SOC: " + str(float(subsystems.battery_subsys.voltageToSOC(subsystems.realworld_subsys.dataPull.batteryVoltage) * 100)) + "% | Voltage: "+ str(subsystems.realworld_subsys.dataPull.batteryVoltage) + "V | Distance Traveled: " + str(subsystems.realworld_subsys.dataPull.distance) + " Miles")
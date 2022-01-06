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
    time = 0 #TODO Initialize properly
    class real():
        batteryVoltage = 0 #TODO Initialize properly
        solarWattage = 0 #TODO Initialize properly
        motorCurrent  = 0 #TODO Initialize properly
    
    class model():
        batteryVoltage = 0 #TODO Initialize properly
        solarWattage = 0 #TODO Initialize properly
        motorCurrent  = 0 #TODO Initialize properly
    # How you can work with data: dataHolding.real.batteryVoltage = 10

def mainControlLoop():
    #Freeze time
    dataHolding.time = 0 #TODO pull real time

    #Pull real worlds into temp
    dataHolding.real.batteryVoltage = subsystems.realworld_subsys.dataPull.batteryVoltage #TODO Confirm syntax when writing realworld subsys
    dataHolding.real.solarWattage = subsystems.realworld_subsys.dataPull.solarWattage #TODO Confirm syntax when writing realworld subsys
    dataHolding.real.motorCurrent = subsystems.realworld_subsys.dataPull.motorCurrent #TODO Confirm syntax when writing realworld subsys
    
    #Pull models into temp
    dataHolding.model.batteryVoltage = subsystems.battery_subsys.dataPull.batteryVoltage #TODO Confirm syntax when writing battery subsys
    dataHolding.model.solarWattage = subsystems.solar_subsys.dataPull.solarWattage #TODO Confirm syntax when writing solar subsys
    dataHolding.model.motorCurrent = subsystems.motor_subsys.dataPull.motorCurrent #TODO Confirm syntax when writing motor subsys
    
    #TODO Run error/log sub system
    subsystems.error_log_subsys.errorComparator()

    #TODO Decide if throttle correction is required

#TODO loop this as frequently as required in config
mainControlLoop()
#E37U

import logging

from sqlalchemy import null
import subsystems.error_log_subsys
import subsystems.battery_subsys
import subsystems.solar_subsys
import subsystems.realworld_subsys
import subsystems.motor_subsys
import sys
import time

import modules.configmodule
#logging.critical('Watch out!')  # will print a message to the console
#logging.warning('I told you so')  # will not print anything


def errorComparator(input):
    #Pull data from input and give it better names
    realBatteryVoltage = input.real.batteryVoltage
    realMotorCurrent  = input.real.motorCurrent
    realPosition = input.real.position

    modelBatterySOC = input.model.batterySOC
    modelMotorCurrent  = input.model.motorCurrent

    #throttleMax = modules.configmodule.config['Throttle']['throttle_hard_max']
    motorCurrentMax = float(modules.configmodule.config['Throttle']['motor_amp_max'])
    batteryVoltageMin = float(modules.configmodule.config['Battery']['battery_low_voltage'])
    if realMotorCurrent > motorCurrentMax:
        class3Error()
        return
    if realBatteryVoltage > batteryVoltageMin:
        class3Error()
        return
    return

def initialChecks():
    batteryV = subsystems.realworld_subsys.dataPull.batteryVoltage
    position = subsystems.realworld_subsys.dataPull.position
    if batteryV > 0 and position != null:
        return
    else:
        class2Error()
        return

def class1Error():
    # Major System Failure
    sys.exit("Class 1 Error")
def class2Error():
    # Real World Failure
    if modules.configmodule.config['Error Override']['c2e_override'] == True:
        print("Class 2 Error OVERRIDE")
        return
    sleepTime = modules.configmodule.config['Errors']['c2e_timout']
    print("Class 2 Error: Real world failure, check physicals")
    time.sleep(sleepTime)
    subsystems.motor_subsys.setThrottle(0)
    time.sleep(sleepTime)
    return
def class3Error():
    # Large discrepancy
    if modules.configmodule.config['Error Override']['c3e_override'] == True:
        print("Class 3 Error OVERRIDE")
        return
    print("Class 3 Error: Large model discrepancy")
    return

def class3Error(): ##DEPRECIATED
    # Internet Failure
    if modules.configmodule.config['Error Override']['c4e_override'] == True:
        print("Class 4 Error OVERRIDE")
        return
    print("Class 4 Error: Internet failure")
    return

def class5Error():
    # Pessimistic Model
    if modules.configmodule.config['Error Override']['c5e_override'] == True:
        print("Class 5 Error OVERRIDE")
        return
    print("Class 5 Error: Pessimistic Model")
    return
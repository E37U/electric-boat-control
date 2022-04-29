#E37U

from sqlalchemy import null
import subsystems.error_log_subsys
import subsystems.battery_subsys
import subsystems.realworld_subsys
import subsystems.motor_subsys
import sys
import time

import modules.configmodule


def errorComparator(input):
    #Pull data from input and give it better names
    realBatteryVoltage = input.real.batteryVoltage
    realMotorCurrent  = input.real.motorCurrent
    realPosition = input.real.position

    modelBatterySOC = input.model.batterySOC
    modelMotorCurrent  = input.model.motorCurrent

    motorCurrentMax = float(modules.configmodule.config['Throttle']['motor_amp_max'])
    batteryVoltageMin = float(modules.configmodule.config['Battery']['battery_low_voltage'])
    if realMotorCurrent > motorCurrentMax: #Check for motor tollerances
        class3Error()
        return
    if realBatteryVoltage > batteryVoltageMin: #Check for battery tolerances
        class3Error()
        return
    return

def initialChecks(): #bootup checks
    batteryV = subsystems.realworld_subsys.dataPull.batteryVoltage
    position = subsystems.realworld_subsys.dataPull.position
    if batteryV > 0 and position != null:
        return
    else:
        class2Error()
        return


#Error codes

def class1Error():
    # Major System Failure
    sys.exit("Class 1 Error")
def class2Error():
    # Real World Failure
    if bool(modules.configmodule.config['Error Override']['c2e_override']) == True:
        return
    sleepTime = modules.configmodule.config['Errors']['c2e_timout']
    print("Class 2 Error: Real world failure, check physicals")
    time.sleep(sleepTime)
    subsystems.motor_subsys.setThrottle(0)
    time.sleep(sleepTime)
    return
def class3Error():
    # Large discrepancy
    if bool(modules.configmodule.config['Error Override']['c3e_override']) == True:
        return
    else:
        print("Class 3 Error: Large model discrepancy")
        return

def class4Error(): ##DEPRECIATED
    # Internet Failure
    if bool(modules.configmodule.config['Error Override']['c4e_override']) == True:
        return
    print("Class 4 Error: Internet failure")
    return

def class5Error():
    # Pessimistic Model
    if bool(modules.configmodule.config['Error Override']['c5e_override']) == True:
        return
    print("Class 5 Error: Pessimistic Model")
    return
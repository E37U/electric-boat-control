#E37U

#https://docs.python.org/3/library/configparser.html#customizing-parser-behaviour
import configparser

config = configparser.ConfigParser(allow_no_value=True)

config.optionxform = str
config.add_section('Position')
config.set('Position', '# Threshold of distance between position points required to register new distance traveled [feet]')
config.set('Position', 'distance_traveled_threshold', '20')

config.add_section('Loop Times')
config.set('Loop Times', '# Time between loops [seconds]')
config.set('Loop Times', 'main_loop_frequency', '30')

config.set('Loop Times', '# Time between real world data pulls (except positional data) [seconds]')
config.set('Loop Times', 'real_world_pull_frequency', '30')

config.set('Loop Times', '# Time between positional data pulls [seconds]')
config.set('Loop Times', 'position_pull_frequency', '10')

config.set('Loop Times', '# Time between internet data pulls [seconds]')
config.set('Loop Times', 'internet_pull_frequency', '120')

config.add_section('Model')
config.set('Model', '# Allowed discrepancy between real and model battery state [HHH UNIT]') #TODO Add units
config.set('Model', 'allowed_battery_model_discrepancy', '10')

config.set('Model', '# Allowed discrepancy between real and model throttle state [HHH UNIT]') #TODO Add units
config.set('Model', 'allowed_throttle_model_discrepancy', '10')

config.set('Model', '# Allowed discrepancy between real and model solar [HHH UNIT]') #TODO Add units and elaborate
config.set('Model', 'allowed_solar_model_discrepancy', '10')

config.add_section('Battery')
config.set('Battery', '# Battery desired low voltage [volts]')
config.set('Battery', 'battery_low_voltage', '1.2')

config.set('Battery', '# Battery emergency low voltage [volts]')
config.set('Battery', 'battery_emergency_low_voltage', '1.1')

config.set('Battery', '# End of race reserve [percent]')
config.set('Battery', 'battery_reserve', '5')

config.add_section('Throttle')
config.set('Throttle', '# Throttle hard max [percent]')
config.set('Throttle', 'throttle_hard_max', '100')

config.set('Throttle', '# Motor amp max [amps]')
config.set('Throttle', 'motor_amp_max', '200')

config.add_section('Race')
config.set('Race', '# Race length [miles]')
config.set('Race', 'race_length', '25')

config.add_section('Errors')
config.set('Errors', '# Class 2 error motor timeout (seconds)')
config.set('Errors', 'c2e_timout', '30')

config.add_section('Error Override')
config.set('Error Override', '#THE FOLLOWING PARAMETERS ARE NOT RECCOMENDED')
config.set('Error Override', '# Class 2 error hard override [bool]')
config.set('Error Override', 'c2e_override', 'False')

config.set('Error Override', '# Class 3 error hard override [bool]')
config.set('Error Override', 'c3e_override', 'False')

config.set('Error Override', '# Class 4 error hard override [bool]')
config.set('Error Override', 'c4e_override', 'False')

config.set('Error Override', '# Class 5 error hard override [bool]')
config.set('Error Override', 'c5e_override', 'False')


with open('config.ini', 'w') as configfile:
    config.write(configfile)
print('We ran!')

#This is how you use this
#modules.configmodule.config.read('config.ini')
#print(modules.configmodule.config.sections())
#print('bit' in modules.configmodule.config.sections())
#print(modules.configmodule.config['Race']['race_length'])
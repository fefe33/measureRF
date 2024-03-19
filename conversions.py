#Functions for [changeme]radio_calculations.py

#m for m to in
#i for in to m

#ONLY TAKES INCHES OR METERS#
def translate_intersystem(value, ismeters:bool):
    if ismeters:
        #if the unit is m return value times the conversion factor
        return value*39.37001
    else:
        #''' same values, opposite operation
        return value/39.37001



#detects the system in use. onlt takes 1 unit
def autodetect_system(unit):
    i, m = ['yd', 'ft', 'in'], ['km', 'm', 'cm', 'mm']
    if unit in i:
        return 'imperial'
    elif unit in m:
        return 'metric'
    else:
        return False

#functions to change units within the same system
def resize_metric(value, u_in, u_out):
    #if the units are the same, save some work and return the same value
    if u_in == u_out:
        return value

    metric_factors = {
        'km': {'km': 1, 'm': 1000, 'cm': 100000, 'mm': 1000000},
        "m": {'km': 0.001, 'm': 1, 'cm': 100, 'mm': 1000},
        "cm": {'km': 0.00001, 'm': 0.01, 'cm': 1, 'mm': 10},
        "mm": {'km': 0.000001, 'm': 0.001, 'cm': 0.1, 'mm': 1}
    }
    return value * metric_factors[u_in][u_out]

def resize_imperial(value, u_in, u_out):
    # if the units are the same, save some work and return the same value
    if u_in == u_out:
        return value
    imperial_factors = {
        'in': {'in': 1, 'ft': 1 / 12, 'yd': 1 / 36},
        'ft': {'in': 12, 'ft': 1, 'yd': 1 / 3},
        'yd': {'in': 36, 'ft': 3, 'yd': 1}
    }
    return value * imperial_factors[u_in][u_out]



#this only translates within the same system
#translate a unit to a different unit based on the given system (imperial or metric)
def translate(value, unit_in, unit_out):
    #autodetect each unit's system
    unit_systems = [autodetect_system(unit_in), autodetect_system(unit_out)]
    if False in unit_systems:
        err = []
        if not unit_systems[0]:
            err.append(unit_in)
        if not unit_systems[1]:
            err.append(unit_out)
        print(f'unsupported unit(s) detected: {err}\nsupported imperial units: [\'in\', \'ft\', \'yd\']\nsupported metric units: [\'km\', \'m\', \'cm\', \'mm\']')
        exit(0)
    '''
        --- this is the start of the actual calculations ---

    '''
    valid_systems = ['imperial', 'metric']
    #if the unit systems are the same
    if unit_systems[0] == unit_systems[1]:
        #if imperial...
        if unit_systems[0] == valid_systems[0]:
            return resize_imperial(value, unit_in, unit_out)
        #if metric
        else:
            return resize_metric(value, unit_in, unit_out)
    else:
        #if the initial value is imperial...
        if unit_systems[0] == valid_systems[0]:
            #get the value as inches
            as_in = resize_imperial(value, unit_in, 'in')
            #convert it to meters:
            as_m = translate_intersystem(as_in, False)
            return resize_metric(as_m, 'm', unit_out)
        else:
            # get the value as meters
            as_m = resize_metric(value, unit_in, 'm')
            # convert it to inches:
            as_in = translate_intersystem(as_m, True)
            return resize_imperial(as_in, 'in', unit_out)

#function to translate value between frequencies (hz)
def translate_frequency(value, unit_in, unit_out):
    unit_factors = {
        'hz':{'hz':1, 'khz':1/1000, 'mhz': 1/1000000},
        'khz':{'hz':1000, 'khz': 1, 'mhz': 1/1000},
        'mhz':{'hz': 1000000, 'khz':1000, 'mhz': 1}
    }
    return value * unit_factors[unit_in][unit_out]


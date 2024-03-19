#some functions for converting between frequency and wavelenth

import sys
from conversions import translate, translate_frequency


def banner():
    banner_text = f'''
    
                ]\\\\    //[  ||###]    //\\\\    /^^^$\\   [|    |]  |]`^`\\\\  ||###]    |]`^`\\\\  |]'*#]
                ] M\\  // [  ||***]   /_**_\\   |#\\__    [|    |]  |]___//  ||***]    |]___//  ||\\__.
         ---    ]  \\\\/m  [  ||      //^^^^\\\\      |\\   [|    |]  || \\\\    ||        || \\\\    ||        ---
                ]        [  ||###] //      \\\\ P/__||   \\\\####//  ||  \\b#  ||###]    ||  \\rr# ||
    
    
    MeasureRF -- by __noobHaxker__ (aka fefe33)
    A simple tool to calculate wavelength from frequency and frequency from wavelength
    '''
    help_text = '''
        
    
        syntax as follows:
            to display this help message:
                --help

            to calculate wavelength from frequency:
                --frequency <value> <input_unit> <output_unit>
                

            to calculate frequency from wavelength:
                --wavelength <value> <input_unit> <output_unit> 


            to convert between supported distance units:
                --convert-distance <value> <input_unit> <output_unit>

            to convert between supported frequency units:
                --convert-frequency <value> <input_unit> <output_unit>
            
            to round the output:
                --round <digits>
                * remember to add this flag AFTER the value your converting and the input/output units  
                
                
        
    '''
    print(banner_text, help_text)

#get all args.
args = sys.argv[1:]

#if there are no args, exit.
if len(args) == 0:
    print('no args supplied. see --help for options')
    exit(0)

#this is the speed of light
SOL = 299792458
#these are the program's currently supported units [these are only for validation on the front end. change back end (conversions.py) to add/ remove conversion factors and other stuff]
valid_dist_units = ['km', 'm', 'cm', 'mm', 'in', 'ft', 'yd']
valid_frequency_units = ['hz', 'khz', 'mhz']

#return the frequency of the specified wavelength ()
def get_frequency(wavelength, unit_in, unit_out):
    s = []
    if unit_in not in valid_dist_units:
        s.append(unit_in)
    if unit_out not in valid_frequency_units:
        s.append(unit_out)
    if len(s) > 0:
        print(f'unsupported unit(s) detected: {s}\nfor distance use: {valid_dist_units},\nfor frequency, use: {valid_frequency_units}\n\nNOTE: the \'--wavelength\' flag converts from <distance> to <frequency>')
        exit(0)

    #convert to m
    m = translate(wavelength, unit_in, 'm')
    #convert to hz
    hz = SOL / m
    #convert to unit_out
    return [translate_frequency(hz, 'hz', unit_out), f' {unit_out}']
    #frequency from wavelength. returns value in hz

def get_wavelength(freq, unit_in, unit_out):
    s = []
    if unit_in not in valid_frequency_units:
        s.append(unit_in)
    if unit_out not in valid_dist_units:
        s.append(unit_out)
    if len(s) > 0:
        print(f'unsupported unit(s) detected: {s}\nfor distance use: {valid_dist_units},\nfor frequency, use: {valid_frequency_units}\n\nNOTE: the \'--wavelength\' flag converts from <frequency> to <distance>')
        exit(0)


    #translate to hz
    hz = translate_frequency(freq, unit_in, 'hz')
    #convert to m
    m = SOL / hz
    #convert to unit_out and return
    return [translate(m, 'm', unit_out), f' {unit_out}']






# main program
def main():
    #if there are less than 4 commands exit and print what went wrong


    #define commands
    valid_cmds = [ '--help', '--frequency', '--wavelength', '--convert-distance', '--convert-frequency', '--round']

    if args[0] not in valid_cmds:
        print(f'argument {args[0]} is not a valid argument. see --help for help with syntax.')
        exit(0)

    #regular validaton:
    #less than 4 args when not using the --help flag breaks the program
    if len(args) < 4 and '--help' not in args:
        print('not enough args supplied. use --help for help with syntax.')
        exit(0)

    #with round validation
    #if the round flag is applied, the args list has to be of length 6
    if '--round' in args and len(args) != 6:
        print('--round flag specified with no value. see \'--help\' for help with syntax')
        exit(0)
    elif '--round' in args and len(args) == 6:
        is_rounded = True
        #try to convert last arg to integer
        try:
            args[5] = int(args[5])
        except:
            print('use integers with the --round flag. see --help option for help with syntax')
            exit(0)

    cmds = {
        '--convert-frequency':translate_frequency,
        '--convert-distance':translate,
        '--frequency':get_frequency,
        '--wavelength':get_wavelength,
        '--help':banner,
        '--round':round
    }


    #if user not asking for help...
    if '--help' not in args and args[0] != '--help':
        #add rounding functionality
        #if the --round argument is supplied round to (argv[5]) digits



        #run the args against the commands
        value = cmds[args[0]](float(args[1]), args[2], args[3])

        #declare this as a variable so i dont have to type it a million times
        r = '--round' in args and args[4] == '--round'

        if args[0] == '--wavelength':
            if r:
                #if the fourth arg is '--round', input that into the function stored at cmds[args[4]] with args[5] as the last argument
                print(f'full:\t\t{str(cmds[args[4]](value[0], args[5])) + value[1]}\nhalf:\t\t{str(cmds[args[4]](value[0]/ 2, args[5])) + value[1]}\nquarter:\t{str(cmds[args[4]](value[0] / 4, args[5])) + value[1]}')
            else:
                print(f'full:\t\t{str(value[0]) + value[1]}\nhalf:\t\t{str(value[0] / 2) + value[1]}\nquarter:\t{str(value[0] / 4) + value[1]}')

        elif args[0] == '--convert-distance' or args[0] == '--convert-frequency':
            if r:
                print(str(cmds[args[4]](value, args[5])) + f' {args[3]}')
            else:
                print(str(value) + f' {args[3]}')
        else:
            if r:
                print(str(cmds[args[4]](value[0], args[5])) + value[1])
            else:
                print(str(value[0]) + value[1])


    else:
        #just to make sure its the right gd value (again) so it doesnt break.
        args[0] ='--help'
        cmds[args[0]]()



main()

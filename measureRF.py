#some functions for converting between frequency and wavelenth

import sys
from conversions import translate, translate_frequency


def banner():
    banner_text = f'''
    
                ]\\\\    //[  ||###]    //\\\\    /^^^$\\   [|    |]  |]`^`\\\\  ||###]    |]`^`\\\\  |]'*#]
                ] M\\  // [  ||***]   /_**_\\   |#\\__    [|    |]  |]___//  ||***]    |]___//  ||\\__.
         ---    ]  \\\\/m  [  ||      //^^^^\\\\      |\\   [|    |]  || \\\\    ||        || \\\\    ||        ---
                ]        [  ||###] //      \\\\ P/__||   \\\\####//  ||  \\b#  ||###]    ||  \\rr# ||
    
    
    MeasureRF -- by __noobHaxker__
    A simple tool to calculate wavelength from frequency and frequency from wavelength
    shame on all the devs who couldnt put together a website that could do this that wasnt either only over HTTP or filled with annoying ads.
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
    #define commands
    valid_cmds = [ '--help', '--frequency', '--wavelength', '--convert-distance', '--convert-frequency']

    if args[0] not in valid_cmds:
        print(f'argument {args[0]} is not a valid argument. see --help for help with syntax.')
        exit(0)



    cmds = {
        '--convert-frequency':translate_frequency,
        '--convert-distance':translate,
        '--frequency':get_frequency,
        '--wavelength':get_wavelength,
        '--help':banner
    }
    #if user not asking for help...
    if '--help' not in args and args[0] != '--help':
        #run the args against the commands
        value = cmds[args[0]](float(args[1]), args[2], args[3])
        if args[0] == '--wavelength':
            print(f'full:\t{str(value[0]) + value[1]}\nhalf:\t{str(value[0]/2) + value[1]}\nquarter:\t{str(value[0]/4) + value[1]}')
        elif args[0] == '--convert-distance' or args[0] == '--convert-frequency':
            print(str(value) + f' {args[3]}')
        else:
            print(str(value[0]) + value[1])

    else:
        #just to make sure its the right gd value (again) so it doesnt break.
        args[0] ='--help'
        cmds[args[0]]()



main()
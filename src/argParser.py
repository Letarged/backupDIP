import argparse
import os
import sys
import appdirs
from termcolor import colored

def get_config_location():
    config_dir_in_this_system = appdirs.user_config_dir("dipconf")
    destination_cfg_file_run = os.path.join(config_dir_in_this_system, "run.cfg")
    destination_cfg_file_dipmodules = os.path.join(config_dir_in_this_system, "dipmodules.py")
    response = "The 2 files with the modules description and settings are following: \n\n"
    response += colored("Details on modules:  ", 'white', attrs=['bold']) + destination_cfg_file_dipmodules + "\n"
    response += colored("Turn on/off modules: ", 'white', attrs=['bold']) + destination_cfg_file_run + "\n\n"
    response += "In order to switch specific modules on/off for the next program execution, modify " + colored(destination_cfg_file_run, 'white', attrs=['bold']) + " accordingly.\n"
    response += "If you wish to add module, you need to add a record in  " + colored(destination_cfg_file_run, 'white', attrs=['bold']) + " and specify all the paths as absolute. And of course write the python code for that module.\n\n"
    response += "Alternatively, you can provide the path of either one these files or both of them, on the command, overwritting this deafult location."
    print(response)


def checkfile(filename):
    if not (os.path.isfile(filename) and os.access(filename, os.R_OK)):
        exit_code = 127
        sys.exit("Error {}: File \"{}\" does not exist or is unreadable.".format(exit_code, filename))
            

def process_cmd_arguments():



    parser = argparse.ArgumentParser(
                        prog='Scanex v0.1',
                        description='Program for scanning given targets.',
                        epilog='Usage of this tool for attacking targets without prior mutual consent is illegal. It is the user\'s responsibility to obey all applicable local, state and federal laws.')
    '''
    parser.add_argument('-t', '--type', help="Type of the attack. Default = 1", choices=range(1,3), default=1)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', help="Text file containing list of target. Each target on a new line.")
    group.add_argument('-s', '--single', help="Single target specified. Either an IP or a web address.")

    args = parser.parse_args()
    

    print("-----------------------")
    print(args.type)
    print(group.file)
    '''#####################################################
    sp = parser.add_subparsers(dest='command')

    parser.add_argument('-m', '--modulefile', help="Path of dipmodules file, which overwrite the deafult one.")
    parser.add_argument('-r', '--runconfig', help="Path of run config file, which overwrites the default one.")

    target_as_list = sp.add_parser('LIST', help="Scanning list of target in the given file.")
    target_as_single = sp.add_parser('SINGLE', help="Scanning just one single target specified in the command line.")
    target_none_discovery_mode = sp.add_parser('DISC', help="Target discovery on the available interfaces.")
    conf_description = sp.add_parser('CONF', help="Prints info about location of config file.")

   # target_as_list.add_argument('-f', '--file', help="Location of the file", required=True)
    target_as_list.add_argument('file', help="Location of the non-empty file")
    target_as_list.add_argument('-t', '--type', help="Type of scan. Default=1", choices=['1', '2'], default='1')
    target_as_single.add_argument('address', help="Target address")
    target_as_single.add_argument('-t', '--type', help="Type of scan. Default=1", choices=['1', '2'], default='1')
    target_none_discovery_mode.add_argument('-c', '--cont', choices=['0', '1', '2'], default='0', help="If desired, the script can automatically perform next scan on all the discovered targets. Default = 0 = do not continue")


   # sp_target_as_single_address = sp.add_parser('-s', '--single', help="Single target specified. Either an IP or a web address.")
    #sp_target_as_list = sp.add_parser('-f', '--file', help="Text file containing list of target. Each target on a new line.")

    args = parser.parse_args()

    overwrite = {
        'modulefile' : args.modulefile if 'modulefile' in vars(args) else None,
        'runconfig' : args.runconfig if 'runconfig' in vars(args) else None
    }
    for key in overwrite:
        print(str(key) + " : " + str(overwrite[key]))

    if not vars(args) or len(sys.argv) == 1:
        parser.print_help()
        exit()
   
    if 'file' in vars(args):
        form_of_scan = "list"
    elif 'address' in vars(args):
        form_of_scan = "single"
    elif args.command == 'CONF':
        print("doing conf")
        get_config_location()
        exit()
    else:
        form_of_scan = "discovery"
    


    
    
    """
        If list -> targetS[] must be non-empty, error otherwise.
        If discovery -> that's the only situation when targetS[] -> legally empty.
    """
    

    if form_of_scan == "list":
        checkfile(args.file)
        with open(args.file, 'r') as f:
            targetS = f.read().split()
        if len(targetS) == 0:
            exit("Empty list given.")
    elif form_of_scan == "single":
        targetS = [args.address]
    else:
        targetS = []
        if 'cont' in vars(args):
            args.type = args.cont
        else:
            args.type = 0

    
    
    return args.type, targetS, overwrite
import argparse
import os
import sys
import appdirs
from termcolor import colored
import datetime

def get_config_location():
    """
        Prints instruction on where the configuration-file and module-file are located along with some basic information on how to parametrize functionality of this tool.

        :var response: The final message which is being composed in the function and ultimately printed on the standard output.
        :type response: str
    
    
    """
    config_dir_in_this_system = appdirs.user_config_dir("dipconf")
    destination_cfg_file_run = os.path.join(config_dir_in_this_system, "run.cfg")
    destination_cfg_file_dipmodules = os.path.join(config_dir_in_this_system, "dipmodules.py")
    response = "The 2 files with the modules description and settings are following: \n\n"
    response += colored("Details on modules:  ", 'white', attrs=['bold']) + destination_cfg_file_dipmodules + "\n"
    response += colored("Turn on/off modules: ", 'white', attrs=['bold']) + destination_cfg_file_run + "\n\n"
    response += "In order to switch on/off specific modules for the next program execution, modify " + colored(destination_cfg_file_run, 'white', attrs=['bold']) + " accordingly.\n"
    response += "If you wish to add module, you need to add a record in  " + colored(destination_cfg_file_run, 'white', attrs=['bold']) + " and specify all the paths as absolute. And of course write the python code for that module.\n\n"
    response += "Alternatively, you can provide the path of either one these files or both of them, on the command, overwritting this deafult location. More information can be found using --help option."
    print(response)


def checkfile(filename):
    """
    Check if the given file exist and if it's readable. If not, 

    :param filename: The file being checked.
    :type filename: str
    :raises FileNotFoundError: If the file doesn't exist, the function exits with exit code 127.
    """
    if not (os.path.isfile(filename) and os.access(filename, os.R_OK)):
        exit_code = 127
        sys.exit("Error {}: File \"{}\" does not exist or is unreadable.".format(exit_code, filename))
            

def process_cmd_arguments():

    """
    Process command-line arguments using the argparse python module. More details in --help.

    :returns: Tuple of the type of scan, list of targets, config files, and output managment options, optionally supplied by the user
    :rtype: tuple(int, list, dict, dict)
    
    args.type, targetS, overwrite
    """

    parser = argparse.ArgumentParser(
                        prog='Dipscan v0.1.0',
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
    
    parser.add_argument('-o', '--outputfile', help="File where output will be saved. In not specified, the output won't be written to any file.")
    parser.add_argument('-m', '--modulefile', help="Path of dipmodules file, which overwrite the deafult one.")
    parser.add_argument('-r', '--runconfig', help="Path of run config file, which overwrites the default one.")
    parser.add_argument('-q', '--quiet', help="Suppress output to stdout.", action='store_true')
    parser.add_argument('-i', '--ignorenetworkissues', help="Force to continue even if a network problem was detected. May lead to errors..", action='store_true')

    target_as_list = sp.add_parser('LIST', help="Scanning list of target in the given file.")
    target_as_single = sp.add_parser('SINGLE', help="Scanning just one single target specified in the command line.")
    target_none_discovery_mode = sp.add_parser('DISC', help="Target discovery on the available interfaces.")
    conf_description = sp.add_parser('CONF', help="Prints info about location of config file.")

    target_as_list.add_argument('file', help="Location of the non-empty file")
    target_as_list.add_argument('-t', '--type', help="Type of scan. Default=1", choices=['1'], default='1')
    target_as_single.add_argument('address', help="Target address")
    target_as_single.add_argument('-t', '--type', help="Type of scan. Default=1", choices=['1'], default='1')
    target_none_discovery_mode.add_argument('-c', '--cont', choices=['0', '1'], default='0', help="If desired, the script can automatically perform next scan on all the discovered targets. Default = 0 = do not continue")


    args = parser.parse_args()


    outputmanagement = {
        'outputfile' : args.outputfile if 'outputfile' in vars(args) else None,
        'printtostdout' : False if args.quiet else True
    }

    if outputmanagement['outputfile'] == None and not outputmanagement['printtostdout']:
        exit_code = 110
        sys.exit("Error {}: In case of -q, --quiet option, it is required to supply '-o', '--outputfile'".format(exit_code))
         

    if outputmanagement['outputfile'] != None:
        if not os.path.exists(outputmanagement['outputfile']):
            os.makedirs(os.path.dirname(outputmanagement['outputfile']),exist_ok=True)
        now = datetime.datetime.now()
        date_str = now.strftime("%dth of %B, %H:%M")
        text = "\n" + f"Created on {date_str}." + "\n\n"
        with open(outputmanagement['outputfile'], "w") as f:
            f.write(text)

    force_to_continue_with_network_issue = False
    if args.ignorenetworkissues:
        force_to_continue_with_network_issue = True

    overwrite = {
        'modulefile' : args.modulefile if 'modulefile' in vars(args) else None,
        'runconfig' : args.runconfig if 'runconfig' in vars(args) else None
    }
 

    if not vars(args) or len(sys.argv) == 1:
        parser.print_help()
        exit()
   
    if 'file' in vars(args):
        form_of_scan = "list"
    elif 'address' in vars(args):
        form_of_scan = "single"
    elif args.command == 'CONF':
        get_config_location()
        exit()
    else:
        form_of_scan = "discovery"
    


    
    
    

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

    
    
    return args.type, targetS, overwrite, outputmanagement, force_to_continue_with_network_issue
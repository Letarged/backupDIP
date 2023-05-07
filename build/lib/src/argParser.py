import argparse

def process_cmd_arguments(debug_on):
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
    parser
    sp = parser.add_subparsers()

    target_as_list = sp.add_parser('LIST', help="Scanning list of target in the given file.")
    target_as_single = sp.add_parser('SINGLE', help="Scanning just one single target specified in the command line.")
    target_none_discovery_mode = sp.add_parser('DISC', help="Target discovery on the available interfaces.")

   # target_as_list.add_argument('-f', '--file', help="Location of the file", required=True)
    target_as_list.add_argument('file', help="Location of the non-empty file")
    target_as_list.add_argument('-t', '--type', help="Type of scan. Default=1", choices=['1', '2'], default='1')
    target_as_single.add_argument('address', help="Target address")
    target_as_single.add_argument('-t', '--type', help="Type of scan. Default=1", choices=['1', '2'], default='1')
    target_none_discovery_mode.add_argument('-c', '--cont', choices=['0', '1', '2'], default='0', help="If desired, the script can automatically perform next scan on all the discovered targets. Default = 0 = do not continue")


   # sp_target_as_single_address = sp.add_parser('-s', '--single', help="Single target specified. Either an IP or a web address.")
    #sp_target_as_list = sp.add_parser('-f', '--file', help="Text file containing list of target. Each target on a new line.")

    args = parser.parse_args()


   
    if 'file' in vars(args):
        form_of_scan = "list"
    elif 'address' in vars(args):
        form_of_scan = "single"
    else:
        form_of_scan = "discovery"
    


    
    
    """
        If list -> targetS[] must be non-empty, error otherwise.
        If discovery -> that's the only situation when targetS[] -> legally empty.
    """
    if form_of_scan == "list":
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

    
    if debug_on: print("targetS: " + str(targetS))
    if debug_on: print("args.type: " + str(args.type))
    return args.type, targetS
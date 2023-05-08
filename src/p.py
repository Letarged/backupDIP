#!/usr/bin/python3
import sys
import os
from os import sys, path
# if __name__ == "__main__":
#     import os, sys
#     sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#     from . import argParser 
#     from . import scanCoordination
# else:
#     import argParser 
#     import scanCoordination


#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Good page for NMAP 
# https://securitytrails.com/blog/nmap-commands 

import src.argParser as argParser
import src.scanCoordination as scanCoordination
import time 
import socket

def check_connected():
    try:
        # connect to the Google DNS server
        socket.create_connection(("8.8.8.8", 53))
        return True
    except:
        sys.stderr.write("Warning: It seem like there is some issue with the internet connection.")
    return False


start_time = time.time()

def main():
    if not os.getuid() == 0:
        exit_code = 126
        sys.exit("Error {}: The tool must be executed as a superuser. Exiting now..".format(exit_code))

    print("\n\n")
    check_connected()
    scanType, targetS, overwritten = argParser.process_cmd_arguments()


    """

    Different meaning of "scanType" variable:

        targetS == []  ->   scanType determins what's happening AFTER potentional targets are discovered
        targetS != []  ->   scanType determins wheter we are running scan1 or scan2 on the given targets

    """

    if targetS == []:
        scanCoordination.performScanType0(scanType, overwritten)
    else:
        match scanType:
            case '1':
                scanCoordination.performScanType1(targetS, overwritten)
            case '2':
                scanCoordination.performScanType2(targetS)
            case _:
                print("Incorrect place in the multiverse.")

    end_time = time.time()
    print("\nDone in " + str("{:.4f}".format(end_time - start_time)) + " seconds.")

    exit()

if __name__ == '__main__':
    main()

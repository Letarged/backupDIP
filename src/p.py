#!/usr/bin/python3

# ------------------------------
# File: ./src/p.py
# Description: Main module containing main function
#
# Mster's Thesis: Tool for Automated Penetration Testing of Web Servers
# Year: 2023
# Tool: dipscan v0.1.0
# Author: Michal Rajecký
# Email: xrajec01@stud.fit.vutbr.cz
#
# BRNO UNIVERSITY OF TECHNOLOGY
# FACULTY OF INFORMATION TECHNOLOGY
# ------------------------------


import sys
import os
from os import path
from termcolor import colored



import src.argParser as argParser
import src.scanCoordination as scanCoordination
import time 
import socket

def check_connected(force_to_continue_with_network_issue):
    """
    Check if there is a connection to the internet by establishing a connection to 8.8.8.8:53. 
    """
    try:
        # connect to the Google DNS server
        socket.create_connection(("8.8.8.8", 53))
        return True
    except:
        if force_to_continue_with_network_issue:
            sys.stderr.write(colored("Warning: It seem like there is some issue with the internet connection.\n", 'red'))
        else:
            exit_code = 99
            sys.exit("Error {}: There is an issue with the internet connection. Exiting now.. if you want to force to continue, use the \"-i\" option.\n".format(exit_code))
    return False


start_time = time.time()

    
def main():
    """
    Takes care of the execution of the whole program. 

    First check if this tool is run as a superusper (which is mandatory in order to work at all). 
    Next check network connection and eventually print a warning. 
    Following by parsing command-line arguments, which determine which type of scan with what argument will take place.
    Additionally, the ``main`` function measures the real-world time and prints the result in second on the command line.

    :var targetS: A list of targets specified by the user. If empty, it means the DISCOVERY scan will take place.
    :type targetS: list

    :var scanType: Can have two meanings. If ``targetS`` == [], meaning DISCOVERY scan has been initialized, it determines what's happening after discovering potential targets. However, if `targetS`` != [], then the discovery doesn't take place and one of a scan types is immediately run on those targets.
    :type scanType: int

    """
 
    if not os.getuid() == 0:
        exit_code = 126
        sys.exit("Error {}: The tool must be executed as a superuser. Exiting now..".format(exit_code))

    scanType, targetS, overwritten, outputmanagment, force_to_continue_with_network_issue = argParser.process_cmd_arguments()
    check_connected(force_to_continue_with_network_issue)


    

  

    if targetS == []:
        scanCoordination.performScanType0(scanType, overwritten, outputmanagment)
    else:
        match scanType:
            case '1':
                scanCoordination.performScanType1(targetS, overwritten, outputmanagment)
            case _:
                print("Incorrect place in the multiverse.")

    end_time = time.time()
    
    print("\nDone in " + str("{:.4f}".format(end_time - start_time)) + " seconds.")

    if outputmanagment['outputfile'] != None:
        print("Output saved into: " + str(outputmanagment['outputfile']))

    exit()

if __name__ == '__main__':
    main()

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

debug_on = False
start_time = time.time()

def main():
    check_connected()
    scanType, targetS = argParser.process_cmd_arguments(debug_on)


    """

    Different meaning of "scanType" variable:

        targetS == []  ->   scanType determins what's happening AFTER potentional targets are discovered
        targetS != []  ->   scanType determins wheter we are running scan1 or scan2 on the given targets

    """

    if targetS == []:
        scanCoordination.performScanType0(scanType, debug_on)
    else:
        match scanType:
            case '1':
                scanCoordination.performScanType1(targetS, debug_on)
            case '2':
                scanCoordination.performScanType2(targetS, debug_on)
            case _:
                print("Incorrect place in the multiverse.")

    end_time = time.time()
    print("\nDone in " + str("{:.4f}".format(end_time - start_time)) + " seconds.")

    exit()

if __name__ == '__main__':
    main()

"""
for x in target_addr.not_closed_not_filtered_ports():
    match x.num:


        case 21:
            funcs.checkForFtpAnon(target_addr)


        case 443:
            print("It's 443")
            sh_result = funcs.shcheckScan(target_addr, x) 
            print("Missing: " + str(sh_result[0].missing))
            cewl_result = funcs.cewlScan(target_addr, x) # TODO možno zbytočne dávať port ako argument? To isté aj v ostatných prípadoch?
            print("Cewl first 10: " + str(cewl_result[:10]))
        
           # whatweb_result = funcs.whatwebScan(target_addr)
           # masscan_result = funcs.masscanScan(target_addr)
            #print(masscan_result)
          #  dnsrecon_result = funcs.dnsreconScan(target_addr)
           # print(whatweb_result)

          #  gobuster_result = funcs.gobusterScan(target_addr, x) # TODO možno zbytočne dávať port ako argument? To isté aj v ostatných prípadoch?
            ssl_results = funcs.nmapSSLScan(target_addr)
            #print(ssl_results)
            print("{" + "\n".join("{!r}: {!r},".format(k, v) for k, v in ssl_results.items()) + "}")


        case 80:
            print("It's 80")
        case _:
            print("Default action... :D " + str(x))




 Toto asi nič 

for x in target_list.ports:
    if x.state == "open":
        funcs.deeperScan(target_list, x)
"""
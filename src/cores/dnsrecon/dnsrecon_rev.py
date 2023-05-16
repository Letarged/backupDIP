# ------------------------------
# File: ./src/cores/dnsrecon/dnsrecon_rev.py
# Description: Module providing functionallity for dnsrecon_rev module
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

from src.secondary.dipmodules import modules
from src.dckrChiefExecutive import launchTheScan
from src.cores.helper import check_ip_or_url, ip_to_range
import socket

def craftDnsReverseLookupCommand(target, port, params):
    output_format = '--json=/dev/stdout'
    if check_ip_or_url(target) == "ip":
        dns_target = target
    elif check_ip_or_url(target) == "url":
        dns_target = socket.gethostbyname(target)
    else:
         dns_target = ""
        
        
   
    dns_target = ip_to_range(dns_target)


    command = (
        output_format +
        " " +
        params +
        " -r " +
        str(dns_target)
    )
    return command


# def run(target,port, modulename, params):
    
#     dnsrecon_command = craftDnsReverseLookupCommand(target, params, output_format)
#     result = launchTheScan(
#         modules[modulename], 
#         dnsrecon_command, 
#         )
#     print(result)

"""
PRidať DO modules 'craft output' a 'medzikrok-output-format'
Tym sa odstrani nutnost pisat launchTheScan() do kazdeho ModuleNotFoundError

Potom sa pozriet na FTP anon
"""
# ------------------------------
# File: ./src/cores/dnsrecon/dnsrecon_cl.py
# Description: Module providing functionallity for dnsrecon module
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
from src.cores.helper import check_ip_or_url
import socket

def craftDnsreconCommand(target, port, params):
    output_format = '--json=/dev/stdout'


    if check_ip_or_url(target) == "ip":
        try: 
            dns_target = socket.gethostbyaddr(target)[0]
        except:
            return ""
    elif check_ip_or_url(target) == "url":
        dns_target = target
    else:
         dns_target = ""
        

    command = (
        output_format +
        " " +
        params +
        " " +
        " -d " +
        str(dns_target)
    )
    return command


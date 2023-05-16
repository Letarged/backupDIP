# ------------------------------
# File: ./src/cores/helper.py
# Description: Auxiliary functions for modules
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

import ipaddress
from urllib.parse import urlparse


def ip_to_range(ip):
    if isinstance(ip, int):
        ip = str(ip)
    
    parts = ip.split('.')
    parts = [int(part) for part in parts]
    parts[-1] += 1
    parts = [str(part) for part in parts]
    range_str = ip + '-' + '.'.join(parts)
    
    return range_str


def check_ip_or_url(value):
    try:
        ip = ipaddress.ip_address(value)
        return "ip"
    except:
        return "url"


"""
         https:// 
            +
        target.com
            + 
          :443
"""



def getFullUrl_from_URI(target, port, with_port_suffix):
    if with_port_suffix:
        if port.port_service == "http":
            target = "http://" + str(target) + ":" + str(port.num)
        elif port.port_service == "https":
            target = "https://" + str(target) + ":" + str(port.num)
    else:
        if port.port_service == "http":
            target = "http://" + str(target)
        elif port.port_service == "https":
            target = "https://" + str(target)

    return target

def getFullUrl(target, port, with_port_suffix):
    if with_port_suffix:
        if port.port_service == "http":
            target = "http://" + str(target.address) + ":" + str(port.num)
        elif port.port_service == "https":
            target = "https://" + str(target.address) + ":" + str(port.num)
    else:

        if port.port_service == "http":
            target = "http://" + str(target.address)
        elif port.port_service == "https":
            target = "https://" + str(target.address)

    return target


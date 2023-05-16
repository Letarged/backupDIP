# ------------------------------
# File: ./src/secondary/scanCoordinationAssistant.py
# Description: 
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
import socket
import src.classes as classes

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
    
def craftHostDiscoveryNmapCommand(target, config, output_format):

    command = (
        output_format +
        " " +
        config['TypeOfScan']['params'] +
        " " +
        target

    )
    return command, config['TypeOfScan']['params']


def craftNmapCommand(target, config, output_format):
    ports_to_scan = config['Nmap_s']['ports']

   
    ports_to_command = ports_to_scan \
        if ports_to_scan[:11] == "--top-ports" \
        else "-p" + ports_to_scan
    nmap_command = (
        output_format +
        " " +
        config['Nmap_s']['params'] +
        " " +
        ports_to_command +
        " " +
        target


    )
    return nmap_command, config['Nmap_s']['params']


def craftMasscanCommand(target, config, output_format):
    if check_ip_or_url(target) == "url":
        target = socket.gethostbyname(target)

    ports_to_scan = config['Masscan_s']['ports']

    
    ports_to_command = ports_to_scan \
        if ports_to_scan[:11] == "--top-ports" \
        else "-p" + ports_to_scan

    masscan_command = (
        output_format +
        " " +
        config['Masscan_s']['params'] +
        " " +
        ports_to_command +
        " " +
        target
    )
    return masscan_command, config['Masscan_s']['params']
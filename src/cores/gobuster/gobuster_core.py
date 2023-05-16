# ------------------------------
# File: ./src/cores/gobuster/gobuster_core.py
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

from src.secondary.dipmodules import modules
from src.dckrChiefExecutive import launchTheScan
from src.cores.helper import check_ip_or_url, getFullUrl_from_URI
import socket
import src.classes as classes

def craftGobusterCommand(target, port, params):
   # gobuster_target = getFullUrl(target, port,1)

    if check_ip_or_url(target) == "ip":
        tmp_trgt = socket.gethostbyaddr(target)[0]

        x = classes.ip(tmp_trgt, port)
        gobuster_target = getFullUrl_from_URI(x, port, 1)
    elif check_ip_or_url(target) == "url":
        gobuster_target = getFullUrl_from_URI(target, port, 1)
    else:
         gobuster_target = ""
        

    command = (
        # "dir " +
        params +
        " " +
        " -u " + gobuster_target
    )

    return command




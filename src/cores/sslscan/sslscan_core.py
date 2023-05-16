# ------------------------------
# File: ./src/cores/sslscan/sslscan_core.py
# Description: Module providing functionallity for sslscan module
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
from src.cores.helper import getFullUrl_from_URI
from termcolor import colored

def craftSSLSCANCommand(target, port, params):
    ssl_target = getFullUrl_from_URI(target, port, 1)
    command = (
        params + 
        " " + 
        ssl_target #+ 

    )
    return command


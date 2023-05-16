# ------------------------------
# File: ./src/cores/nmap/nmapssl.py
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


def craftNmapSSLCommand(target, port, params):
    output_format = '-oX -'

    command = (
        output_format +
        " " +
        params +
        " " +
        "-p " + str(port.num) +
        " " +
        target

    )

    return command



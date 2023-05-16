# ------------------------------
# File: ./src/cores/whatweb/whatweb_core.py
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

from calendar import c
from src.secondary.dipmodules import modules
from src.cores.helper import getFullUrl_from_URI
from src.dckrChiefExecutive import launchTheScan


def craftWhatwebCommand(target, port, params):
    output_format = '--log-json=- -q'
    whatweb_target = getFullUrl_from_URI(target, port, 1)
    command = (
        output_format +
        " " +
        params +
        " " +
        whatweb_target
    )
    return command


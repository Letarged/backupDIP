# ------------------------------
# File: ./src/cores/shcheck/shckech_core.py
# Description: Module providing functionallity for shcheck module
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
from src.cores.helper import getFullUrl_from_URI
from src.dckrChiefExecutive import launchTheScan



def craftShcheckCommand(target, port, params):
    output_format='--json-output'
    shcheck_target = getFullUrl_from_URI(target, port, 0)
    command = (
        output_format + 
        " " +
        params +
        " " +
        " -p" + str(port.num) +
        " " +
        shcheck_target
    )
    return command 


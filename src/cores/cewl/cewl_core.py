# ------------------------------
# File: ./src/cores/cewl/cewl_core.py
# Description: Module providing functionallity for cewl module
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
import os
import requests


def possible_to_connect_to_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # If the response was successful, no Exception will be raised
        return True
    except:
        return False

def craftCewlCommand(target, port, outputfile):
    cewl_target = getFullUrl_from_URI(target, port, 1)
    command = (
        
        cewl_target 
    )

    return command



def run(cmd, target, port, module,print_according_to_outputmanagment, outputmanagment):
    if not possible_to_connect_to_url(getFullUrl_from_URI(target, port, 1)):
        print("Not possible to connect to: " + str(getFullUrl_from_URI(target, port, 1)))
        return
    result = launchTheScan(
        module, 
        cmd, 
        )

    dest_folder_to_write_wordlist_to = module['outputfolder']
    dest_file_to_write_wordlist_to = os.path.join(module['outputfolder'],target) + "_cewl.out"
    
    if not os.path.exists(dest_folder_to_write_wordlist_to):
            os.makedirs(dest_folder_to_write_wordlist_to)
    with open(dest_file_to_write_wordlist_to, "w") as file:
        for element in result:
            file.write(element + "\n")
    print_according_to_outputmanagment(outputmanagment, colored("Custom word list (port " + str(port.num) + ") generated into: ", 'blue') + colored(dest_file_to_write_wordlist_to, 'green'))
from src.secondary.dockerimages import modules
from src.dckrChiefExecutive import launchTheScan
from src.cores.helper import getFullUrl_from_URI
from termcolor import colored

def craftCewlCommand(target, port, params, outputfile):
    cewl_target = getFullUrl_from_URI(target, port, 1)
    command = (
        str(params) +
        " " +
        cewl_target #+ 
       # " -w " +
        #outputfile
    )
    print(command)
    return command



def run(target,port, modulename, params):
    command = craftCewlCommand(target, port, params, modules[modulename]['outputfile'])
    result = launchTheScan(
        modules[modulename], 
        command, 
        )

    with open(modules[modulename]['outputfile'], "w") as file:
        for element in result:
            file.write(element + "\n")
    print(colored("Custom word list generated into: ", 'grey') + colored(modules[modulename]['outputfile'], 'green'))
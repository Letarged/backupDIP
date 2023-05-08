from src.secondary.dockerimages import modules
from src.dckrChiefExecutive import launchTheScan
from src.cores.helper import getFullUrl_from_URI
from termcolor import colored

def craftCewlCommand(target,port,params):
    cewl_target = getFullUrl_from_URI(target, port, 1)
    command = (
        str(params) +
        " " +
        cewl_target
    )
    return " --help >> /dev/null"


def craftCewlCommand2(target, port, outputfile):
    cewl_target = getFullUrl_from_URI(target, port, 1)
    command = (
        
        cewl_target + 
        " -w " +
        outputfile
    )
    return command



# def run(target,port, modulename, params):
def run(cmd, target, port, module):
    command = craftCewlCommand2(target, port, module['outputfile'])
    result = launchTheScan(
        module, 
        command, 
        )

    with open(module['outputfile'], "w") as file:
        for element in result:
            file.write(element + "\n")
    print(colored("Custom word list generated into: ", 'grey') + colored(module['outputfile'], 'green'))
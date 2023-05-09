from src.secondary.dipmodules import modules
from src.dckrChiefExecutive import launchTheScan
from src.cores.helper import getFullUrl_from_URI
from termcolor import colored
import os

# def craftCewlCommand(target,port,params):
#     cewl_target = getFullUrl_from_URI(target, port, 1)
#     command = (
#         str(params) +
#         " " +
#         cewl_target
#     )
#     return " --help >> /dev/null"


def craftCewlCommand(target, port, outputfile):
    cewl_target = getFullUrl_from_URI(target, port, 1)
    command = (
        
        cewl_target 
    )
    return command



# def run(target,port, modulename, params):
def run(cmd, target, port, module,print_according_to_outputmanagment, outputmanagment):
   # command = craftCewlCommand(target, port, module['outputfolder'])
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
    # print(colored("Custom word list generated into: ", 'grey') + colored(module['outputfolder'], 'green'))
    print_according_to_outputmanagment(outputmanagment, colored("Custom word list generated into: ", 'blue') + colored(dest_file_to_write_wordlist_to, 'green'))
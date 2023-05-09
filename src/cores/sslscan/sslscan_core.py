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
       # " -w " +
        #outputfile
    )
    return command


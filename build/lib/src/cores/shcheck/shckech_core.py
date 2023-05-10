from src.secondary.dipmodules import modules
from src.cores.helper import getFullUrl_from_URI
from src.dckrChiefExecutive import launchTheScan



def craftShcheckCommand(target, port, params):
    output_format='--json-output'
    # print(target)
    # print(port)
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


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

# def run(target, port, modulename,params ):
    
#     whatweb_result = launchTheScan(
#         modules[modulename],
#         whatweb_cmd
#     )
#     print(whatweb_result)
#     return
    
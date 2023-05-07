from src.secondary.dockerimages import modules
from src.cores.helper import getFullUrl_from_URI
from src.dckrChiefExecutive import launchTheScan



def craftShcheckCommand(target, port, params, output_format):
    print(target)
    print(port)
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


# def run(target,port, modulename):
#     try:
#         output_format='--json-output'
#         params = modules[modulename]['params']
#         """ Following line ensures that shcheck will get https://site.org and not IP address, because in that case shcheck gives an error"""
#         print("UA")
#         shcheck_command = craftShcheckCommand(target, port, params, output_format)
#         print("UA")
#         shcheck_result = launchTheScan(
#             modules[modulename], 
#             shcheck_command, 
#             )
#     except:
#         shcheck_result = "Err"

#     print(shcheck_result)

def run(target,port, modulename, params):
   
    output_format='--json-output'
    """ Following line ensures that shcheck will get https://site.org and not IP address, because in that case shcheck gives an error"""
    shcheck_command = craftShcheckCommand(target, port, params, output_format)
    shcheck_result = launchTheScan(
        modules[modulename], 
        shcheck_command, 
        )
    
    print(shcheck_result)
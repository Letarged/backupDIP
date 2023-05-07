
from src.secondary.dockerimages import modules
from src.dckrChiefExecutive import launchTheScan


def craftNmapSSLCommand(target, port, params, output_format):
    command = (
        output_format +
        " " +
        params +
        " " +
        "-p " + str(port.num) +
        " " +
        target

    )

    return command



def run(target,port, modulename, params):
    output_format = '-oX -'
    dnsrecon_command = craftNmapSSLCommand(target, port, params, output_format)
    result = launchTheScan(
        modules[modulename], 
        dnsrecon_command, 
        )
    print(result)
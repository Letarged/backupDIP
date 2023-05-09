
from src.secondary.dipmodules import modules
from src.dckrChiefExecutive import launchTheScan


def craftNmapSSLCommand(target, port, params):
    output_format = '-oX -'

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



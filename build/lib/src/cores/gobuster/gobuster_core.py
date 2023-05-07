from src.secondary.dockerimages import modules
from src.dckrChiefExecutive import launchTheScan
from src.cores.helper import check_ip_or_url, getFullUrl_from_URI
import socket
import src.classes as classes

def craftGobusterCommand(target, port, params, wordlist):
   # gobuster_target = getFullUrl(target, port,1)

    if check_ip_or_url(target) == "ip":
        tmp_trgt = socket.gethostbyaddr(target)[0]

        x = classes.ip(tmp_trgt, port)
        gobuster_target = getFullUrl_from_URI(x, port, 1)
    elif check_ip_or_url(target) == "url":
        gobuster_target = getFullUrl_from_URI(target, port, 1)

    command = (
        # "dir " +
        params +
        " " +
        " -w " + wordlist +
        " -u " + gobuster_target
    )

    print(command)
    return command



def run(target,port, modulename, params):
    command = craftGobusterCommand(target, port, params, modules[modulename]['wordlist'])
    result = launchTheScan(
        modules[modulename], 
        command, 
        )

    print(result)
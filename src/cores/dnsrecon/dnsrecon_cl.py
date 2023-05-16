
from src.secondary.dipmodules import modules
from src.dckrChiefExecutive import launchTheScan
from src.cores.helper import check_ip_or_url
import socket

def craftDnsreconCommand(target, port, params):
    output_format = '--json=/dev/stdout'


    if check_ip_or_url(target) == "ip":
        try: 
            dns_target = socket.gethostbyaddr(target)[0]
        except:
            return ""
    elif check_ip_or_url(target) == "url":
        dns_target = target
    else:
         dns_target = ""
        

    command = (
        output_format +
        " " +
        params +
        " " +
        " -d " +
        str(dns_target)
    )
    return command


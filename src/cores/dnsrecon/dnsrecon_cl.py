
from src.secondary.dockerimages import modules
from src.dckrChiefExecutive import launchTheScan
from src.cores.helper import check_ip_or_url
import socket

def craftDnsreconCommand(target, params, output_format):

    if check_ip_or_url(target) == "ip":
        dns_target = socket.gethostbyaddr(target)[0]
    elif check_ip_or_url(target) == "url":
        dns_target = target
        

    command = (
        output_format +
        " " +
        params +
        " " +
        " -d " +
        str(dns_target)
    )
    return command


def run(target,port, modulename, params):
    output_format = '--json=/dev/stdout'
    dnsrecon_command = craftDnsreconCommand(target, params, output_format)
    result = launchTheScan(
        modules[modulename], 
        dnsrecon_command, 
        )
    print(result)
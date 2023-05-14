import ipaddress
from urllib.parse import urlparse
import socket
import src.classes as classes

def ip_to_range(ip):
    """
    Converts an IPv4 address to an IP range of 2 IPs, starting with the given IP
    and ending with the IP which is plus one. For example 8.8.8.8-8.8.8.9
    
    Args:
    - ip (str or int): the IPv4 address to convert
    
    Returns:
    - range_str (str): the IP range as a string
    """
    # Convert the IP to a string if it's an integer
    if isinstance(ip, int):
        ip = str(ip)
    
    # Split the IP into its four parts
    parts = ip.split('.')
    
    # Convert each part to an integer
    parts = [int(part) for part in parts]
    
    # Increment the last part of the IP
    parts[-1] += 1
    
    # Convert each part back to a string
    parts = [str(part) for part in parts]
    
    # Join the parts back together with dots to form the IP range
    range_str = ip + '-' + '.'.join(parts)
    
    return range_str


def check_ip_or_url(value):
    try:
        ip = ipaddress.ip_address(value)
        return "ip"
    except:
        return "url"


"""
         https:// 
            +
        target.com
            + 
          :443
"""



def getFullUrl_from_URI(target, port, with_port_suffix):
    if with_port_suffix:
        if port.port_service == "http":
            target = "http://" + str(target) + ":" + str(port.num)
        elif port.port_service == "https":
            target = "https://" + str(target) + ":" + str(port.num)
    else:
        if port.port_service == "http":
            target = "http://" + str(target)
        elif port.port_service == "https":
            target = "https://" + str(target)

    return target

def getFullUrl(target, port, with_port_suffix):
    if with_port_suffix:
        if port.port_service == "http":
            target = "http://" + str(target.address) + ":" + str(port.num)
        elif port.port_service == "https":
            target = "https://" + str(target.address) + ":" + str(port.num)
    else:
        if port.port_service == "http":
            target = "http://" + str(target.address)
        elif port.port_service == "https":
            target = "https://" + str(target.address)

    return target


def craftGobusterCommand(target, port, config):
   # gobuster_target = getFullUrl(target, port,1)

    if check_ip_or_url(target.address) == "ip":
        tmp_trgt = socket.gethostbyaddr(target.address)[0]

        x = classes.ip(tmp_trgt, port)
        gobuster_target = getFullUrl(x, port, 1)
    elif check_ip_or_url(target.address) == "url":
        gobuster_target = getFullUrl(target, port, 1)

    command = (
        # "dir " +
        config['Gobuster']['params'] +
        " " +
        " -w " + config['Gobuster']['wordlist'] +
        " -u " + gobuster_target
    )

    # print(command)
    return command, config['Gobuster']['params']


def craftWhatwebCommand(target, port, config, output_format):
    whatweb_target = getFullUrl_from_URI(target, port, 1)
    command = (
        output_format +
        " " +
        config['Whatweb']['params'] +
        " " +
        #     config['Whatweb']['aggression'] +
        " " +
        # "-p" + str(port.num) +
        " " +
        whatweb_target

    )
    return command, config['Whatweb']['params']


def craftNmapSSLCommand(target, port, config, output_format):
    command = (
        output_format +
        " " +
        config['Nmapssl']['params'] +
        " " +
        "-p " + str(port.num) +
        " " +
        str(target.address)

    )

    return command, config['Nmapssl']['params']


def craftCewlCommand(target, port, config):
    cewl_target = getFullUrl(target, port, 1)
    command = (
        config['Cewl']['params'] +
        " " +
        cewl_target

    )
    return command, config['Cewl']['params']


def craftDnsreconCommand(target, config, output_format):

    if check_ip_or_url(target.address) == "ip":
        dns_target = socket.gethostbyaddr(target.address)[0]
    elif check_ip_or_url(target.address) == "url":
        dns_target = target.address
        

    command = (
        output_format +
        " " +
        config['Dnsrecon']['params'] +
        " " +
        " -d " +
        str(dns_target)
    )
    return command, config['Dnsrecon']['params']

def craftDnsReverseLookupCommand(target, config, output_format):

    if check_ip_or_url(target.address) == "ip":
        dns_target = target.address
    elif check_ip_or_url(target.address) == "url":
        dns_target = socket.gethostbyname(target.address)[0]
        
    dns_target = ip_to_range(dns_target)


    command = (
        output_format +
        " " +
       # config['Dnsrecon']['params'] +
        " " +
        " -r " +
        str(dns_target)
    )
    return command, '-r'



def craftShcheckCommand(target, port, config, output_format):
    
    shcheck_target = getFullUrl(target, port, 0)
    command = (
        output_format +
        " -d " +
        config['Shcheck']['params'] +
        " -p" + str(port.num) +
        " " +
        shcheck_target
    )
    return command, config['Shcheck']['params']


def craftHostDiscoveryNmapCommand(target, config, output_format):

    command = (
        output_format +
        " " +
        config['TypeOfScan']['params'] +
        " " +
        target

    )
    return command, config['TypeOfScan']['params']


def craftNmapCommand(target, config, output_format):
    ports_to_scan = config['Nmap_s']['ports']

    # if "--top-ports 10" is specified, leave it like that
    # but if "21,22,80,443,8080" is specified, we need to add "-p" prefix for nmap
    ports_to_command = ports_to_scan \
        if ports_to_scan[:11] == "--top-ports" \
        else "-p" + ports_to_scan
    nmap_command = (
        output_format +
        " " +
        config['Nmap_s']['params'] +
        " " +
        ports_to_command +
        " " +
        target


    )
    return nmap_command, config['Nmap_s']['params']


def craftMasscanCommand(target, config, output_format):
    if check_ip_or_url(target) == "url":
        target = socket.gethostbyname(target)

    ports_to_scan = config['Masscan_s']['ports']

    # if "--top-ports 10" is specified, leave it like that
    # but if "21,22,80,443,8080" is specified, we need to add "-p" prefix for nmap
    ports_to_command = ports_to_scan \
        if ports_to_scan[:11] == "--top-ports" \
        else "-p" + ports_to_scan

    masscan_command = (
        output_format +
        " " +
        config['Masscan_s']['params'] +
        " " +
        ports_to_command +
        " " +
        target
    )
    # print(masscan_command)
    return masscan_command, config['Masscan_s']['params']
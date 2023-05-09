import ipaddress
from urllib.parse import urlparse


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


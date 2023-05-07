from enum import Enum




"""
class PortState(Enum):
    NDEF = 0
    OPEN = 1
    filtered = 2
    CLOSED = 3
    UNFILTERED = 4
    OPENFILTERED = 5
    CLOSEDFILTERED = 6
"""

class port:
    def __init__(self, num, state, port_service):
        if not isinstance(num, int):
            raise Exception("Port num must be -int-")
        self.num = num
        self.state = state
        self.port_service = port_service
        # Default service is always being set according to the nmap (not hardcoded - in case something changes)
        

    def __str__(self):
        return (str(self.num) + " : " + str(self.state) + " :: " + str(self.port_service))

class ip:
    def __init__(self, ipaddr, ports=None):
        self.address = ipaddr
        if ports == None:
            self.ports = []
        else:
            self.ports = ports

    def not_closed_not_filtered_ports(self):
        lst = []
        for port in self.ports:
            if port.state != "closed" and port.state != "filtered":
                lst.append(port)
        return lst

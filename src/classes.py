# ------------------------------
# File: ./src/classes.py
# Description: Auxiliary classes
#
# Mster's Thesis: Tool for Automated Penetration Testing of Web Servers
# Year: 2023
# Tool: dipscan v0.1.0
# Author: Michal Rajecký
# Email: xrajec01@stud.fit.vutbr.cz
#
# BRNO UNIVERSITY OF TECHNOLOGY
# FACULTY OF INFORMATION TECHNOLOGY
# ------------------------------


from termcolor import colored

class port:
    def __init__(self, num, state, port_service):
        if not isinstance(num, int):
            raise Exception("Port num must be -int-")
        self.num = num
        self.state = state
        self.port_service = port_service
        # Default service is always being set according to the nmap (not hardcoded - in case something changes)
        

    def __str__(self):
        result =  ("\t" + colored(str(self.num), "yellow", attrs=["bold"]) 
        + " : " 
        + (colored(str(self.state) , "green") if str(self.state) == 'open' else colored(str(self.state), "red")) 
        + " :: "
        + colored(str(self.port_service), "blue", attrs=["bold"]))
        return result

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

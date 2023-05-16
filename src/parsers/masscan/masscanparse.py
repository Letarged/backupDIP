# ------------------------------
# File: ./src/parsers/masscan/masscanparse.py
# Description: Functions for running masscan module
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

import json
import src.classes as classes

# this is needed because there is no service name in the masscan output, unlike in the case of nmap
# and later in the process of the execution the program is matching service name, not the port number
port_mapping = {
    "80": "http",
    "443": "https",
    "53": "domain",
    "22": "ssh",
    "3389": "ms-wbt-server",
    "445": "microsoft-ds",
    "139": "netbios-ssn",
    "137": "netbios-ns",
    "23": "telnet",
    "25": "smtp",
    "8080": "http-proxy",
    "21": "ftp",
    "110": "pop3",
    "143": "imap",
    "3306": "mysql",
    "1723": "pptp",
    "111": "rpcbind",
    "995": "pop3s",
    "993": "imaps",
    "5900": "vnc",
    "1025": "msrpc",
    "587": "submission",
    "8888": "sun-answerbook",
    "199": "smux",
    "8443": "https-alt",
    "465": "smtps",
    "631": "ipp",
    "2000": "callbook",
    "902": "vmware-auth",
    "5800": "vnc-http",
    "179": "bgp",
    "3690": "svn",
    "10000": "snet-sensor-mgmt",
    "1433": "ms-sql-s",
    "554": "rtsp",
    "32768": "filenet-tms",
    "873": "rsync",
    "49152": "unknown",
    "20031": "bakbonenetvault",
    "5000": "upnp",
    "135": "msrpc",
    "9950": "apc-9950",
    "1026": "msrpc",
    "1030": "iad1",
    "1720": "h323q931",
    "3283": "netassistant",
    "2717": "pn-requester",
    "4899": "radmin",
    "3000": "ppp",
    "5678": "rrac",
    "5666": "nrpe",
    "49153": "unknown",
    "1434": "ms-sql-m",
    "2049": "nfs",
    "6543": "apache-admin",
    "11110": "sgi-lk",
    "5432": "postgresql",
    "8081": "blackice-icecap",
    "49154": "unknown",
    "32771": "sometimes-rpc17",
    "2222": "EtherNetIP-1",
    "20005": "btx",
    "6000": "x11",
    "3268": "globalcatLDAP",
    "9100": "jetdirect",
    "11111": "vce",
    "49155": "unknown",
    "543": "klogin",
    "544": "kshell",
    "389": "ldap",
    "49156": "unknown",
    "25565": "minecraft",
    "5555": "freeciv",
    "808": "ccproxy-http",
    "49157": "unknown",
    "3899": "ith-irms-lm",
}

def make_proper_structure(jsonStr):
    target_ip = jsonStr[0]['ip']
    tmp = []
    for record in jsonStr:     
        one_port = classes.port(int(record['ports'][0]['port']),record['ports'][0]['status'], port_mapping[str(record['ports'][0]['port'])] )
        tmp.append(one_port)

    return tmp, target_ip


def parse_output(output):
    data = ""
    for line in output.logs(stream=True):
        data += line.decode("utf-8")
   
    data = data.split("\n",3)[3].strip() # remove the annoying masscan header lines
    data = data[:data.rfind("\nrate")+1] # remove last line
    
    jsonStr = json.loads(data)

    tmp, target_ip = make_proper_structure(jsonStr)
    return classes.ip(target_ip, tmp)


    if data == "":
        return data, 
    else: 
        # print(jsonStr[1]["ports"])
        return make_proper_structure(jsonStr)
    
# ------------------------------
# File: ./src/parsers/nmap/nmapdiscoveryparse.py
# Description: 
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
import xmltodict
from termcolor import colored



def format_discovered_hosts(ip_list):
    output = colored('Discovered hosts:\n', attrs=['bold'])
    for ip in ip_list:
        output += f"        {colored(ip, 'green')}\n"
    return output


def nmap_output_proccess_sn(jsonStr):
  tmp = []
  for i in jsonStr["nmaprun"]["host"]:
      tmp.append(i["address"]["@addr"])

  return tmp
  


def parse_output(output):
  data = ""
  
  for line in output.logs(stream=True):
      data += line.decode("utf-8")
  data = json.dumps(xmltodict.parse(data), indent=4)
  jsonStr = json.loads(data)
  lst = nmap_output_proccess_sn(jsonStr)
  return (format_discovered_hosts(lst), lst)
    
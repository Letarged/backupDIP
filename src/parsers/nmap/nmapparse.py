# ------------------------------
# File: ./src/parsers/nmap/nmapparse.py
# Description: Functions for running nmap module
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

import src.classes as classes # user-defined module

def n_hosts_up(jsonStr):
    num = int(jsonStr['nmaprun']['runstats']['hosts']['@up'])
    return num

def nmap_output_proccess(jsonStr):
  
  target_ip_address = jsonStr["nmaprun"]["host"]["address"]["@addr"]
  tmp = []

  if "port" not in jsonStr["nmaprun"]["host"]["ports"]:
    return None, target_ip_address

  if isinstance(jsonStr["nmaprun"]["host"]["ports"]["port"], dict):
    jsonStr["nmaprun"]["host"]["ports"]["port"] = [jsonStr["nmaprun"]["host"]["ports"]["port"]]

  for i in jsonStr["nmaprun"]["host"]["ports"]["port"]:
      if not "service" in i:
        continue

      one_port = classes.port(int(i["@portid"]),i["state"]["@state"],i["service"]["@name"] )
      tmp.append(one_port)


  return tmp ,target_ip_address

def parse_output(output):

    data = ""
    for line in output.logs(stream=True):
        data += line.decode("utf-8")
    
    data = json.dumps(xmltodict.parse(data), indent=4)
    jsonStr = json.loads(data)
    if n_hosts_up(jsonStr) == 0:
      return None
    # print(jsonStr)
    tmp, target_ip = nmap_output_proccess(jsonStr)

    return classes.ip(target_ip, tmp)
    
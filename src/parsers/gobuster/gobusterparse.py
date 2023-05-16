# ------------------------------
# File: ./src/parsers/gobuster/gobusterparse.py
# Description: Functions for running gobuster module
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

import re
import json

class Cgobuster:
    def __init__(self, code ,lst_of_targets):
        self.code = code
        self.lst_of_targets = lst_of_targets

def parse_output(output):
    data = ""
    for line in output.logs(stream=True):
        data += line.decode("utf-8")
   # print(data)
    pattern = r".*\(Status:\s.*"
    
    tmp = data.split('\n')
    tmp = tmp[1:]
    array = {}
    for x in tmp:
        if re.fullmatch(pattern, x):
            array[x.split(" (Status: ")[0]] = \
            int(x.split(" (Status:")[1].replace(')', ''))
                
                
       
    unique_codes_received = list(set(list(array.values())))
    print(unique_codes_received)


    unique_codes_received.append(200)
    unique_codes_received.append(202)
    unique_codes_received.append(401)
    final_output = {}
    for code in unique_codes_received:
        final_output[code] = [k for k, v in array.items() if v == code] # all the elements with the same return code
   


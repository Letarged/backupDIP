# ------------------------------
# File: ./src/parsers/whatweb/whatwebparse.py
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
from termcolor import colored


def extract_info_from_json(data):
    output = ''
    for record in data:
        if record['http_status'] == 200:
            output += 'Target: ' + colored(record['target'], 'green') + '\n'
            output += 'IP: ' + colored(record['plugins']['IP']['string'][0], 'yellow') + '\n'
            output += 'Country: ' + colored(record['plugins']['Country']['module'][0], 'magenta') + '\n'
            output += 'Email: ' + colored(record['plugins'].get('Email', {'string': ['']})['string'][0], 'cyan') + '\n'
            output += 'JQuery: ' + colored(record['plugins'].get('JQuery', {'version': ['']})['version'][0], 'blue') + '\n'
            output += 'Uncommon headers: ' + colored(', '.join(record['plugins'].get('UncommonHeaders', {'string': ['']})['string']), 'red') + '\n'
            output += 'X-Frame-Options: ' + colored(record['plugins'].get('X-Frame-Options', {'string': ['']})['string'][0], 'green') + '\n'
            output += '\n'
    return output


def parse_output_basic(output):
    data = ""
    for line in output.logs(stream=True):
        data += line.decode("utf-8")
    
   

    """
        This Json is an array of results, so each record is an element in the array.
        In order to access to the results, we need to specify [index].
    
    """
    try:
        jsonStr = json.loads(data)
    except:
        return ""
 
    
    return extract_info_from_json(jsonStr)


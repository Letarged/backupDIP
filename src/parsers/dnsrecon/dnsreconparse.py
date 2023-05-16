# ------------------------------
# File: ./src/parsers/dnsrecon/dnsreconparse.py
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



def extract_txt_records(data):
    try:
        txt_records = [record for record in data['TXT']]
    except:
        return ""
    output = colored('TXT records:\n', 'blue')
    for record in txt_records:
        name = record['name']
        string = record['strings']
        output += f"     Name: {colored(name, 'green')}, String: {colored(string, 'yellow')}\n"
    return output

def extract_txt_fields(data):
    txt_records = data.get('TXT')
    if txt_records is None:
        return []
    extracted_fields = []
    for record in txt_records:
        name = record.get('name')
        strings = record.get('strings')
        if name is not None and strings is not None:
            extracted_fields.append((name, strings))
    return extracted_fields

def group_by_type(records):
    result = {}
    for record in records:
        record_type = record["type"]
        if record_type in result:
            result[record_type].append(record)
        else:
            result[record_type] = [record]
    return result

def parse_output(output):
    data = ""
    for line in output.logs(stream=True):
        data += line.decode("utf-8")
    data = data.split("[*]", 1)[0]

   

    jsonStr = json.loads(data)


    return (extract_txt_records(group_by_type(jsonStr)))

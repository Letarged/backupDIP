# ------------------------------
# File: ./src/parsers/dnsrecon/dnsreverseparse.py
# Description: Functions for running dnsreverse module
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


def extract_ptr_records(json_data):
    ptr_records = json_data[1]
    ptr_output = colored("PTR (reverse lookup) records:\n", "blue")
    for record in ptr_records:
        address = record["address"]
        name = record["name"]
        ptr_output += f"     Address: {colored(address, 'green')}, Name: {colored(name, 'magenta')}\n"
    return ptr_output


def parse_output(output):
    data = ""
    for line in output.logs(stream=True):
        data += line.decode("utf-8")
    data = data.split("[*]", 1)[0]

    jsonStr = json.loads(data)

    return extract_ptr_records(jsonStr)

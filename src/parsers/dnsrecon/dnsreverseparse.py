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

    # print("DATA: " + str(data))
    jsonStr = json.loads(data)

    return extract_ptr_records(jsonStr)
    # finish testing and organizing json output

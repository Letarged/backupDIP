import json
import xmltodict
from termcolor import colored

def extract_common_name(json_str):
    # Convert the JSON string to a Python dictionary
   # data = json.loads(json_str)

    # Extract the value of the "tldr" key
    tldr = json_str.get("tldr", "")

    # Extract the "commonName" value from the "tldr" string
    start_index = tldr.find("commonName=")
    if start_index == -1:
        return ""

    end_index = min(tldr.find(",", start_index), tldr.find("\n", start_index))
    if end_index == -1:
        end_index = len(tldr)

    common_name = tldr[start_index + len("commonName="):end_index]

    return common_name

def print_ssl_cert_info(json_output):
    # extract important values from json
    ip = json_output.get('ip', '')
    common_name = json_output.get('commonName', '')
    org_name = json_output.get('organizationName', '')
    bits = json_output.get('bits', '')
    not_before = json_output.get('notBefore', '')
    not_after = json_output.get('notAfter', '')
    sans = json_output.get('subjectAltName', [])
    typeofcert = json_output.get('type_of_cert', '')
    sigalgo = json_output.get('sig_algo', '')
    issuer = json_output.get('issuer', '')

    # format output string
    output = colored(f"SSL cert for ", 'light_grey') + colored(f"{ip}", 'yellow') + colored(":\n", 'grey')
    if common_name:
        output += colored(f"    {colored('Common Name:', 'white', attrs=['bold'])} {colored(common_name, 'green')}\n")
    if org_name:
        output += colored(f"    {colored('Organization:', 'white', attrs=['bold'])} {colored(org_name, 'green')}\n")
    if issuer:
            output += colored(f"    {colored('Issuer:', 'white', attrs=['bold'])} {colored(issuer, 'green')}\n")
    if bits:
        output += colored(f"    {colored('Bits:', 'white', attrs=['bold'])} {colored(bits, 'green')}\n")
    if not_before and not_after:
        output += colored(f"    {colored('Validity:', 'white', attrs=['bold'])} {colored(f'{not_before} - {not_after}', 'green')}\n")
    if typeofcert:
        output += colored(f"    {colored('Type of Cert:', 'white', attrs=['bold'])} {colored(typeofcert, 'green')}\n")
    if sigalgo:
        output += colored(f"    {colored('Signature alg:', 'white', attrs=['bold'])} {colored(sigalgo, 'green')}\n")
    if common_name:
        output += colored(f"    {colored('commonNAme:', 'white', attrs=['bold'])} {colored(extract_common_name(json_output), 'red')}\n")
    if sans:
        output += colored(f"    {colored('Subject Alternative Names:', 'white', attrs=['bold'])} {colored(', '.join(sans), 'green')}\n")

    return output


def process_ssl_json(jsonSSL):
    tmp = {}
    tmp["ip"] = jsonSSL["nmaprun"]["host"]["address"]["@addr"]
    tmp["iptype"] = jsonSSL["nmaprun"]["host"]["address"]["@addrtype"]
    tmp["hostname"] = jsonSSL["nmaprun"]["host"]["hostnames"]["hostname"]
    tmp["service"] = jsonSSL["nmaprun"]["host"]["ports"]["port"]["service"]
    #tmp["XXX"] =  jsonSSL["nmaprun"]["host"]["ports"]["port"]["script"]["table"][1]["elem"][0]["@key"]
    #tmp[jsonSSL["nmaprun"]["host"]["ports"]["port"]["script"]["table"][1]["elem"][0]["@key"]] = jsonSSL["nmaprun"]["host"]["ports"]["port"]["script"]["table"][1]["elem"][0]["#text"]
    
    size_of_arr = len(jsonSSL["nmaprun"]["host"]["ports"]["port"]["script"]["table"][1]["elem"])
    for i in range(size_of_arr):
        tmp[jsonSSL["nmaprun"]["host"]["ports"]["port"]["script"]["table"][1]["elem"][i]["@key"]] = jsonSSL["nmaprun"]["host"]["ports"]["port"]["script"]["table"][1]["elem"][i]["#text"]
    
    size_of_arr = len(jsonSSL["nmaprun"]["host"]["ports"]["port"]["script"]["table"][2]["elem"])
    for i in range(size_of_arr):
        tmp[jsonSSL["nmaprun"]["host"]["ports"]["port"]["script"]["table"][2]["elem"][i]["@key"]] = jsonSSL["nmaprun"]["host"]["ports"]["port"]["script"]["table"][2]["elem"][i]["#text"]

    size_of_outer_arr = len(jsonSSL["nmaprun"]["host"]["ports"]["port"]["script"]["table"][3]["table"])
    for x in range(size_of_outer_arr):
        size_of_inner_arr = len(jsonSSL["nmaprun"]["host"]["ports"]["port"]["script"]["table"][3]["table"][x]["elem"])
        for y in range(size_of_inner_arr):
            tmp[jsonSSL["nmaprun"]["host"]["ports"]["port"]["script"]["table"][3]["table"][x]["elem"][y]["@key"]] = jsonSSL["nmaprun"]["host"]["ports"]["port"]["script"]["table"][3]["table"][x]["elem"][y]["#text"]

    # valid from:
    tmp[jsonSSL["nmaprun"]["host"]["ports"]["port"]["script"]["table"][4]["elem"][0]["@key"]] = jsonSSL["nmaprun"]["host"]["ports"]["port"]["script"]["table"][4]["elem"][0]["#text"]
    # valid until:
    tmp[jsonSSL["nmaprun"]["host"]["ports"]["port"]["script"]["table"][4]["elem"][1]["@key"]] = jsonSSL["nmaprun"]["host"]["ports"]["port"]["script"]["table"][4]["elem"][1]["#text"]

    size_of_arr = len(jsonSSL["nmaprun"]["host"]["ports"]["port"]["script"]["elem"])
    
    for i in range(size_of_arr):
        tmp[jsonSSL["nmaprun"]["host"]["ports"]["port"]["script"]["elem"][i]["@key"]] = jsonSSL["nmaprun"]["host"]["ports"]["port"]["script"]["elem"][i]["#text"]

    tmp["type_of_cert"] = jsonSSL["nmaprun"]["host"]["ports"]["port"]["script"]["@id"]
    tmp["tldr"] = jsonSSL["nmaprun"]["host"]["ports"]["port"]["script"]["@output"]


    return tmp
def parse_output(output):
    data = ""
    for line in output.logs(stream=True):
        data += line.decode("utf-8")

    
    data = json.dumps(xmltodict.parse(data), indent=4)
    jsonStr = json.loads(data)

    # return (print_ssl_cert_info(jsonStr))
    return(print_ssl_cert_info(process_ssl_json(jsonStr)))

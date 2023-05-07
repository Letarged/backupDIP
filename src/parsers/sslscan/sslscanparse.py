import json
import xmltodict
from termcolor import colored

"""
def check_tls_compression(jsonStr):
    json_string = jsonStr['document']['ssltest']
    # Check if "tlscompression" key is present in the JSON
    if "tlscompression" not in json_string:
        print("HERE")
        return ""
    
    # Check the value of the "allowed" key under "tlscompression"
    allowed = json_string["tlscompression"]["@allowed"]
    if allowed == "0":
        return colored("TLS Compression: ", "green") + colored("not allowed", "green")
    else:
        return colored("TLS Compression: ", "red", attrs=['dark']) + colored("allowed", "red")
"""

def renegotiation_supported(jsonStr):
    json_string = jsonStr['document']['ssltest']
    # print(json_string)
    # exit()
    if "renegotiation" not in json_string:
        print("HERE")
        return ""
    else:
        result = ""
        if json_string["renegotiation"]["@supported"] == "1":
            result += colored("TLS Renegotiation: ", "red", attrs=['dark', 'bold']) + colored("supported", "green")
            if json_string["renegotiation"]["@secure"] == "1":
                result += colored (" (and secure)", "green")
            else:
                result += colored (" (and NOT SECURE)", "red", attrs=['bold'])
        else:
            result = colored("TLS Renegotiation: ", "red", attrs=['dark', 'bold']) + colored("not supported", "green")
    return result

def check_heartbleed_vulnerability(jsonStr):
    json_string = jsonStr['document']['ssltest']
    try:
        if "heartbleed" not in json_string:
            return ""
        vulnerable_sslversions = []
        if "heartbleed" in json_string:
            for sslversion in json_string["heartbleed"]:
                if sslversion.get("@vulnerable") == "1":
                    vulnerable_sslversions.append(sslversion["@sslversion"])        
        if vulnerable_sslversions == []:
            return f'{colored("Heartbleed: ", "red", attrs=["dark", "bold"])}{colored("not vulnerable", "green")}' + "\n"
        else:
            vulnerable_sslversions_string = ", ".join(vulnerable_sslversions)
            return colored(f"Heartbleed: vulnerable ({vulnerable_sslversions_string})", "red", attrs=["bold"]) + "\n"
    except:
        print("EXCEPT")
        return ""

def sort_by_bits(cipher):
    return int(cipher['@bits'])

def extract_cipher_info(data):
    if 'document' not in data or 'ssltest' not in data['document']:
        return ""
    cipher_info = ""
    ''' According to the code on GitHub, each cipher can fall into of the following categories '''
    cipher_strength = {
        'anonymous': [],
        'null': [],
        'weak': [],
        'acceptable': [],
        'medium': [],
        'strong': []
        }
    
    for cipher in data['document']['ssltest']['cipher']:
        if '@strength' in cipher and cipher['@strength'] in cipher_strength:
            cipher_strength[cipher['@strength']].append(cipher)
    for strength in cipher_strength.keys():
        if cipher_strength[strength]:
            cipher_info += colored(f"{strength.capitalize()} ciphers:\n", 'blue', attrs=['bold', 'dark'])
            sorted_ciphers = sorted(cipher_strength[strength], key=sort_by_bits, reverse=True)
            for cipher in sorted_ciphers:
                cipher_info += f"\t{colored(cipher['@sslversion'], 'red')} {colored(cipher['@bits'], 'green', attrs=['dark'])} {colored('bits', 'green', attrs=['dark'])} {colored(cipher['@cipher'], 'cyan')}\n"
    return cipher_info

def extract_enabled_protocols(json_str):
    result = [colored("Enabled protocols:", 'blue', attrs=["bold", "dark"])]
    protocols = json_str["document"]["ssltest"]["protocol"]
    enabled_protocols = []
    for p in protocols:
        if p["@enabled"] == "1":
            enabled_protocols.append(colored(f"              {p['@type']} {p['@version']}", 'blue'))

    result.extend(enabled_protocols)
    return "\n".join(result) + '\n'

def parse_output(output):
 
    data = ""
    for line in output.logs(stream=True):
        data += line.decode("utf-8")
  
    data = json.dumps(xmltodict.parse(data), indent=4)
    jsonStr = json.loads(data)
    result =    extract_enabled_protocols(jsonStr) + \
                extract_cipher_info(jsonStr) + \
                check_heartbleed_vulnerability(jsonStr) + \
                renegotiation_supported(jsonStr)
    return result
    
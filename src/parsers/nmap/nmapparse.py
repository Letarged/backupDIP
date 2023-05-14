import json
import xmltodict

import src.classes as classes # user-defined module

def n_hosts_up(jsonStr):
    # Parse the JSON output from nmap
    # Extract the number of hosts up from the output
    num = int(jsonStr['nmaprun']['runstats']['hosts']['@up'])
    return num

def nmap_output_proccess(jsonStr):
  
  target_ip_address = jsonStr["nmaprun"]["host"]["address"]["@addr"]
  tmp = []

  # if all the scanned ports are closed
  if "port" not in jsonStr["nmaprun"]["host"]["ports"]:
    return None, target_ip_address

  # in case of exactly 1 open port (we need it to be an array of 1 element, not just that 1 element)
  if isinstance(jsonStr["nmaprun"]["host"]["ports"]["port"], dict):
    jsonStr["nmaprun"]["host"]["ports"]["port"] = [jsonStr["nmaprun"]["host"]["ports"]["port"]]

  for i in jsonStr["nmaprun"]["host"]["ports"]["port"]:
      # if there is no service, it should mean the port is closed
      if not "service" in i:
        continue

      one_port = classes.port(int(i["@portid"]),i["state"]["@state"],i["service"]["@name"] )
      tmp.append(one_port)

 # print("TMP: " + str(tmp))
  #print("TARGET IP ADDRESS: " + str(target_ip_address))
  return tmp ,target_ip_address

# bude sa musieť upraviť, lebo nie všetky nástroje majú xmlko ako nmap
# update -> už som to osamostatnil, len ešte stále to je ako keby pripravené robiť switch, to už teda netreba
def parse_output(output):
   # for line in output.logs(stream=True):
        #if debug_on: print(line)
  #  if debug_on: print("#############") 
  #  if debug_on: print("#############") 
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
    
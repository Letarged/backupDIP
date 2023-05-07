import src.funcs as funcs
import netifaces
import ipaddress
import configparser
import src.secondary.scanCoordinationAssistant as assist
import time
import threading
import os
import sys
from termcolor import colored
from src.secondary import dockerimages
from src.secondary.dockerimages import meta
import importlib

settings = configparser.RawConfigParser()
#settings.read('src/secondary/conf/settings.cfg') 
#settings.read(os.path.join(sys.path[0], "src/secondary/conf/settings.cfg"), encoding='utf-8')

def print_banner(address):
    line = "------- " + address + " -------"
    line_len = len(line)
    print("-" * line_len)
    print(line)
    print("-" * line_len)

# also excludes "..._" so for example Masscan And Nmap since that's a whole different cattegory and architectural approach
# also checks if there is a record in modules (dockerImages)
# if not BUT NOT SWITCHED_ON -> warning
# if not AND TRIED TO USE -> error
def get_switched_on(config):
    # enabled_sections = []
    # for section in config.sections():
    #     print(section)
    #     not_eixsting = False
    #     if not module_exists(section):
    #         not_eixsting = True
    #         sys.stderr.write("Warning: module \"" + str(section) + "\" is in config file but not defined (no record)." "\n")
    #     if config.getint(section, 'switched_on') == 1:
    #         if not_eixsting: 
    #             exit_code = 128
    #             sys.exit("Error {}: module \"{}\" switched on but not defined (no record).".format(exit_code, section))
    #         enabled_sections.append(section)


    enabled_sections = []
    for section in config.sections():
        if section[-2:] == '_s': continue # "nmap_s" and "masscan_s" will be ignored
        if not module_exists(section):
            not_eixsting = True
        else:
            not_eixsting = False

        
        if not_eixsting:
            if config.getint(section, 'switched_on') == 1:
                exit_code = 128
                sys.exit("Error {}: module \"{}\" switched on but not defined (no record).".format(exit_code, section))
            else:
          #      sys.stderr.write("Warning: module \"" + str(section) + "\" is in config file but not defined (no record)." "\n")
                pass
        else:
            if config.getint(section, 'switched_on') == 1:
                enabled_sections.append(section)
                
    return enabled_sections

def display_loading():
    counter = 0
    while True:
        if counter % 6 == 0:
            print("\rGobuster in progress ", end="")
        print(".", end="", flush=True)
        time.sleep(0.9)
        counter += 1
        if counter >= 30:
            break


def netmaskToSlash(netmask):
        ip_network = ipaddress.IPv4Network("0.0.0.0/" + netmask, strict=False)
        return ip_network.prefixlen

def getInterfaces(configInterfaces, logic):
    lst = []
    if logic == True:
        for interf in configInterfaces:
            if configInterfaces.getboolean(interf) == False:
                lst.append(interf)
    else:
        for interf in configInterfaces:
            if configInterfaces.getboolean(interf) == True:
                lst.append(interf)
    return lst

"""
    [Logic]
    1 = if an interface is not explicitly forbidden, then it's allowed (even if not listed above)
      = so "lst" is composed of the forbidden interfaces
    0 = allow only those interfaces, which are listed and has "True / 1" value
      = so "lst" is composed of the allowed interfaces

"""
def gonna_be_scanned(lst, interface, logic):
    if logic == True:
        if len(interface) == 2:
            if interface in lst:
                return False
        else:
            if (interface in lst) or (interface[:(len(interface)-1)] in lst):
                return False
        return True
    else:
        if len(interface) == 2:
            if interface in lst:
                return True
        else:
            if (interface in lst) or (interface[:(len(interface)-1)] in lst):
                return True
        return False
    
def module_exists(module_from_config):
    if module_from_config in dockerimages.modules.keys():
        return True
    else:
        return False
    
def portScanningPhase(targetS, config, settings):
    doneAtLeastOneScan = False
    nmap_found_targets = {} 
    masscan_found_target = {}
    if config['Nmap_s'].getboolean('switched_on'):
        doneAtLeastOneScan = True
        for target in targetS:
            nmap_command, param = assist.craftNmapCommand(target, config, settings['NmapOutput']['output'])
            nmap_found_targets[target] = funcs.launchTheScan("nmap", nmap_command, param)
            #if debug_on: print("Went for " + str(target) + str(found_targets[target]))

    if config['Masscan_s'].getboolean('switched_on'):
        doneAtLeastOneScan = True
        for target in targetS:
            masscan_command, param = assist.craftMasscanCommand(target, config, settings['MasscanOutput']['output'])
            masscan_found_target[target] = funcs.launchTheScan("masscan", masscan_command, param)
    
    if not doneAtLeastOneScan:
        exit("At least one scan must be performed:  nmap / masscan")

    to_s_cim_pracujeme = {**masscan_found_target, **nmap_found_targets}

    # for x in list(to_s_cim_pracujeme.keys()):
    #     print("LULU: " + str(x))
    #     for port in to_s_cim_pracujeme[x].not_closed_not_filtered_ports():
    #         print(port)

    #print(str(type(masscan_found_target)))
    #print(nmap_found_targets[next(iter(nmap_found_targets))])
   # print(nmap_found_targets['whiskeyprovsechny.cz'])
   # return(masscan_found_target.update(nmap_found_targets))
    return {**nmap_found_targets, **masscan_found_target}
    #exit()
    # print("THIS: " + str(masscan_found_target.update(nmap_found_targets))) # TODO NAPIČU LEBO NASTANE OVERWRITE (takto to je zatiaľ len ako proforma)

# This is the main function for coordinating type-1-scan
# It should perform all the steps specified in the confing file, 
#       one after antoher, adjusting the steps according 
#       to the results from initial nmap ports discovery
def divideField(txt):
    path = txt.rsplit(".",1)[0]
    func = txt.rsplit(".",1)[1]
    return path, func

def service_check(module_service, real_services):
    if module_service == 'ANY' or module_service in real_services:
        return True
    else:
        return False

def performScanType1(targetS, debug_on):

    config = configparser.RawConfigParser()
    settings = configparser.RawConfigParser()

    dir_path = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(dir_path, "secondary", "conf", "settings.cfg")
    # settings.read('src/secondary/conf/settings.cfg') 
    settings.read(config_file) 
    type_one_file = os.path.join(dir_path, settings['Path']['typeoneConf']) 
    print(type_one_file)
    config.read(type_one_file)
    print(settings.sections())
    
    switched_ons = get_switched_on(config)
    found_targets = portScanningPhase(targetS, config, settings)
    # found_targets = portScanningPhase(targetS, settings)
    # for target in list(found_targets.keys()):
    #     print("HERE: " + str(target) + "  :: " + str(found_targets[target]))
    #     for interestingport in found_targets[target].not_closed_not_filtered_ports():
    #         print(str(target) + " - " + str(interestingport.num) + " " + str(interestingport.port_service))
    
    print(switched_ons)
    

    for target in list(found_targets.keys()):
        print_banner(target)
        if (found_targets[target] == None):
            print(colored("..probably down", 'red'))
            continue
        for switched_on_module in switched_ons:
            print("Going for: " + str(switched_on_module))
            ports = [p for p in found_targets[target].not_closed_not_filtered_ports()]

            for open_port in ports:

            #services = [x.port_service for x in ports]
            #print(switched_on_module)
            #print(str(dockerimages.modules[switched_on_module]))
                if (dockerimages.modules[switched_on_module]['service'] == open_port.port_service):
                    path_of_parser, main_func_inside_module = divideField(dockerimages.modules[switched_on_module]['core'])
                    if main_func_inside_module == 'NONE':
                        print("NO DOCKER RUN FOR: " + str(main_func_inside_module))
                        continue
                    correctModule = importlib.import_module(path_of_parser)
                    try:
                        getattr(
                            correctModule, 
                            main_func_inside_module
                            )(
                                target,
                                open_port, 
                                switched_on_module, 
                                dockerimages.modules[switched_on_module]['params']
                            )
                    except:
                        continue

    return
        
    for target in list(found_targets.keys()):
        print_banner(target)
       
        if (found_targets[target] == None):
            print(colored("..probably down", 'red'))
            continue
        for interestingport in found_targets[target].not_closed_not_filtered_ports():
            match interestingport.port_service:
                case "https":
                        if config['Gobuster'].getboolean('switched_on'):
                            gobuster_command, params = assist.craftGobusterCommand(found_targets[target], interestingport, config)
                            loading_thread = threading.Thread(target=display_loading)
                            loading_thread.start()
                            gobuster_result = funcs.launchTheScan("gobuster", gobuster_command, params)
                            loading_thread.join()
                            # print(gobuster_result)
                            print("Gobuster : " + str(gobuster_result)[:50])

                        if config['Whatweb'].getboolean('switched_on'):
                            # whatweb_command, params = assist.craftWhatwebCommand(found_targets[target], interestingport, config, settings['WhatwebOutput']['output'])
                            whatweb_command, params = assist.craftWhatwebCommand(target, interestingport, config, settings['WhatwebOutput']['output'])
                            whatweb_result=funcs.launchTheScan("whatweb",whatweb_command, params)
                            # print(whatweb_result)
                            print("Whatweb : " + str(whatweb_result))

                        if config['Nmapssl'].getboolean('switched_on'):
                            nmapssl_command, params = assist.craftNmapSSLCommand(found_targets[target], interestingport, config, settings['NmapOutput']['output'])
                            nmapssl_result = funcs.launchTheScan("nmap", nmapssl_command, params) 
                            # print(nmapssl_result)
                            print("Nmapssl : " + str(nmapssl_result)[:50])

                        if config['Cewl'].getboolean('switched_on'):
                            cewl_command, params = assist.craftCewlCommand(found_targets[target], interestingport, config)
                            cewl_result = funcs.launchTheScan("cewl", cewl_command, params)
                            # print(cewl_result)
                            print("Cewl : " + str(cewl_result)[:20])

                        if config['Shcheck'].getboolean('switched_on'):
                            try:
                                """ Following line ensures that shcheck will get https://site.org and not IP address, because in that case shcheck gives an error"""
                                found_targets[target].address = target
                                shcheck_command, params = assist.craftShcheckCommand(found_targets[target], interestingport, config, settings['ShcheckOutput']['output'])
                                shcheck_result = funcs.launchTheScan("shcheck", shcheck_command, params)
                            except:
                                shcheck_result = ""
                            print(shcheck_result)

                case "domain":
                        if config['Dnsrecon'].getboolean('switched_on'):
                            dnsrecon_command, params = assist.craftDnsreconCommand(found_targets[target], config, settings['DnsreconOutput']['output'])
                            dnsrecon_result = funcs.launchTheScan("dnsrecon", dnsrecon_command, params)
                            print(str(dnsrecon_result))
                            dnsrecon_command, params = assist.craftDnsReverseLookupCommand(found_targets[target], config, settings['DnsreconOutput']['output'])
                            dnsrecon_result = funcs.launchTheScan("dnsrecon", dnsrecon_command, params)
                            print(str(dnsrecon_result))
                        
def performScanType0(scan_after_discovery, debug_on):
    
    config = configparser.RawConfigParser()
    config.read(settings['Path']['typezeroConf']) 

    our_interfaces = getInterfaces(config['Interfaces'], config['Logic'].getboolean('negative'))
    interfaces = netifaces.interfaces()

    potentional_targets = []
    for inter in interfaces:
        if gonna_be_scanned(our_interfaces, inter, config['Logic'].getboolean('negative')):
            ip = netifaces.ifaddresses(inter)[netifaces.AF_INET][0]['addr']
            netmask = netifaces.ifaddresses(inter)[netifaces.AF_INET][0]['netmask']
            full_ip = str(ip) + "/" + str(netmaskToSlash(netmask))
           # potentional_targets.append(str(inter) + " : " + str(full_ip))
            potentional_targets.append(str(full_ip))
    # print(potentional_targets)

    for target in potentional_targets:
        discovery_command, parameter = assist.craftHostDiscoveryNmapCommand(target, config,settings['NmapOutput']['output'])
        discovery_result = funcs.launchTheScan("nmap", discovery_command, parameter)
        print(discovery_result[0])
    

    match scan_after_discovery:
        case '0':
            pass
        case '1':
            performScanType1(discovery_result[1], debug_on)
        case '2':
            performScanType2(discovery_command[1], debug_on)


def performScanType2(targetS, debug_on):
    pass 
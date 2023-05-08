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
import importlib.util
import appdirs
from src.dckrChiefExecutive import launchTheScan

settings = configparser.RawConfigParser()
#settings.read('src/secondary/conf/settings.cfg') 
#settings.read(os.path.join(sys.path[0], "src/secondary/conf/settings.cfg"), encoding='utf-8')

def get_type_one_file_because_possible_overwrite(overwrite, dir_path):
    config_dir_in_this_system = appdirs.user_config_dir("dipconf")
    type_one_file_by_default = os.path.join(config_dir_in_this_system, "run.cfg")

    if not overwrite['runconfig'] == None:
        type_one_file = overwrite['runconfig']
    else:
        type_one_file = type_one_file_by_default
        #type_one_file = os.path.join(dir_path, "secondary", "conf", "types", "typeone.cfg") 

    if not is_file_readable(type_one_file):
        sys.stderr.write(colored(f"Warning: file \"{type_one_file}\" doesn't exist or is not readable. Using the defaults.\n", 'red'))
        # type_one_file = os.path.join(dir_path, "secondary", "conf", "types", "typeone.cfg")
        type_one_file = type_one_file_by_default
    print("RETURNING WHAT? " + type_one_file)
    return type_one_file

def get_modules_because_possible_overwrite(overwrite, default_modules):
    if not overwrite['modulefile'] == None:
        module_file_path = overwrite['modulefile']
        if not is_file_readable(module_file_path):
            sys.stderr.write(colored(f"Warning: file \"{module_file_path}\" doesn't exist or is not readable. Using the defaults.\n", 'red'))
            return default_modules
        module_name = os.path.splitext(os.path.basename(module_file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, module_file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if 'modules' not in module.__dict__:
            sys.stderr.write(colored(f"Warning: file \"{module_file_path}\" doesn't contain \"modules\" dict. Using the defaults.\n", 'red'))
        else:
            module_result = module.modules

    else:
        module_result = default_modules

    return module_result

def is_file_readable(filename):
    if os.access(filename, os.R_OK):
        return True
    else:
        return False

def try_to_read_file(filename):
    filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)
    if os.path.exists(filepath):
        print("TRYING TO OPEN: " + filename)
        with open("src/" +filename, "r") as f:
            content = f.read()
            return content
    else:
        print(f"NOT EXISTS: {filepath}.")
        exit()


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
def get_switched_on(config, modules):
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
        if not module_exists(section, modules):
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
    
def module_exists(module_from_config, modules):
    if module_from_config in modules.keys():
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

def performScanType1(targetS, overwrite):

    config = configparser.RawConfigParser()
    settings = configparser.RawConfigParser()


    dir_path = os.path.dirname(os.path.abspath(__file__))

    type_one_file = get_type_one_file_because_possible_overwrite(overwrite, dir_path)
    modules = get_modules_because_possible_overwrite(overwrite, dockerimages.modules)

    settings_file = os.path.join(dir_path, "secondary", "conf", "settings.cfg") 

    config.read(type_one_file)
    settings.read(settings_file)

    print("HERE: " + type_one_file)
    print(settings.sections())
    
    switched_ons = get_switched_on(config, modules)
    print(switched_ons)
    found_targets = portScanningPhase(targetS, config, settings)
    # found_targets = portScanningPhase(targetS, settings)
    # for target in list(found_targets.keys()):
    #     print("HERE: " + str(target) + "  :: " + str(found_targets[target]))
    #     for interestingport in found_targets[target].not_closed_not_filtered_ports():
    #         print(str(target) + " - " + str(interestingport.num) + " " + str(interestingport.port_service))
    
    
    

    for target in list(found_targets.keys()):
        print_banner(target)
        if (found_targets[target] == None):
            print(colored("..probably down", 'red'))
            continue
        for switched_on_module in switched_ons:
            print("Going for: " + str(switched_on_module))
            ports = [p for p in found_targets[target].not_closed_not_filtered_ports()]

            for open_port in ports:

           
                if (modules[switched_on_module]['service'] == open_port.port_service):
                    path_of_parser, main_func_inside_module = divideField(modules[switched_on_module]['core'])
                    if main_func_inside_module == 'NONE':
                        print("NO DOCKER RUN FOR: " + str(main_func_inside_module))
                        # TODO
                        continue
                    path_of_command_cretor, command_creator_fun = divideField(modules[switched_on_module]['command'])
                    correctModule_of_main_fun = importlib.import_module(path_of_parser)
                    correctModule_of_create_command_fun = importlib.import_module(path_of_command_cretor)
                    print("MODULES: " + str(modules[switched_on_module].keys()))
                    
                    
                    try:
                        cmd = getattr(
                                correctModule_of_create_command_fun,
                                command_creator_fun
                                )(
                                    target,
                                    open_port,
                                    modules[switched_on_module]['params']
                                )
                        
                        print()
                        if 'additional' in modules[switched_on_module]:
                            path_of_additional, func_of_additional = divideField(modules[switched_on_module]['additional'])
                            correctModule_of_additional = importlib.import_module(path_of_additional)
                            getattr(
                                correctModule_of_additional,
                                func_of_additional
                            )(
                                cmd,
                                target,
                                open_port,
                                modules[switched_on_module]
                            )
                        if not 'abort_classic' in modules[switched_on_module]: 
                            print(launchTheScan(modules[switched_on_module],cmd))
                    except:
                        print(switched_on_module + " finished with error..")
                        continue
                    
                    # try:
                    #     cmd = getattr(
                    #         correctModule_of_create_command_fun,
                    #         command_creator_fun
                    #         )(
                    #             target,
                    #             open_port,
                    #             modules['params']
                    #         )
                    #     print(switched_on_module + " - CMD: " + cmd)
                    #     exit()
                    #     getattr(
                    #         correctModule_of_main_fun, 
                    #         main_func_inside_module
                    #         )(    print("Este fajn")

                    # except:
                    #     print("UPSIK")
                    #     continue

    return
        
                        
def performScanType0(scan_after_discovery):

    config = configparser.RawConfigParser()
    settings = configparser.RawConfigParser()

    dir_path = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(dir_path, "secondary", "conf", "settings.cfg")
    # settings.read('src/secondary/conf/settings.cfg') 
    settings.read(config_file) 
    type_zero_file = os.path.join(dir_path, settings['Path']['typezeroConf'])
    config = configparser.RawConfigParser()
    config.read(type_zero_file) 

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
            performScanType1(discovery_result[1])
        case '2':
            performScanType2(discovery_command[1])


def performScanType2(targetS):
    pass 
# ------------------------------
# File: ./src/scanCoordination.py
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

import time
import os
import re
import sys
import importlib
import appdirs
import netifaces
import ipaddress
import configparser
import importlib.util
import src.portFuncs as portFuncs
import src.secondary.scanCoordinationAssistant as assist
from termcolor import colored
from src.secondary import dipmodules
from src.dckrChiefExecutive import launchTheScan
from src import classes
# settings = configparser.RawConfigParser()



def safe_import(module_path):
    try:
        x = importlib.import_module(module_path)
        return x
    except:
        path = module_path.rsplit("/", 1)[0]
        module_itself = module_path.split("/")[-1]
        sys.path.append(path)
        return importlib.import_module(module_itself)



def check_correct_form_of_module(module, all_modules):
    if not module in all_modules:
        print("HAPPENED THIS: " + str(module) + " not in " + str(all_modules.keys()))
        exit()
    if not ('image' in all_modules[module] and 'service' in all_modules[module] and 'parser' in all_modules[module]):
        exit_code = 111
        sys.exit("Error {}: Incorrect form of a module {}. Must contain at least \"service\", \"parser\" and \"image\" key.".format(
            exit_code, module))


def print_according_to_outputmanagment(outputmanagment, data):

    if outputmanagment['printtostdout']:
        print(data)
    if outputmanagment['outputfile'] != None:
        write_to_file(outputmanagment['outputfile'], data)


def write_to_file(filename, data):
    with open(filename, 'a') as file:
        print(data, file=file)


def extract_domain_name(url):
    url_without_scheme = re.sub(r'^https?://', '', url).rstrip('/')
    parts = url_without_scheme.split('/', 1)
    return parts[0]


def get_type_one_file_because_possible_overwrite(overwrite, dir_path):
    config_dir_in_this_system = appdirs.user_config_dir("dipconf")
    type_one_file_by_default = os.path.join(
        config_dir_in_this_system, "run.cfg")

    if not overwrite['runconfig'] == None:
        type_one_file = overwrite['runconfig']
    else:
        type_one_file = type_one_file_by_default

    if not is_file_readable(type_one_file):
        sys.stderr.write(colored(
            f"Warning: file \"{type_one_file}\" doesn't exist or is not readable. Using the defaults.\n", 'red'))
        type_one_file = type_one_file_by_default
    return type_one_file


def get_modules_because_possible_overwrite(overwrite, default_modules):
    config_dir_in_this_system = appdirs.user_config_dir("dipconf")
    destination_default_dipmodules = os.path.join(config_dir_in_this_system, "dipmodules.py")

    module_result = default_modules # None WAS
    if not overwrite['modulefile'] == None:
        module_file_path = overwrite['modulefile']
    else:
        module_file_path = destination_default_dipmodules
    
    if not is_file_readable(module_file_path):
        sys.stderr.write(colored(
            f"Warning: file \"{module_file_path}\" doesn't exist or is not readable. Using the defaults.\n", 'red'))
        return default_modules
    module_name = os.path.splitext(os.path.basename(module_file_path))[0]
    spec = importlib.util.spec_from_file_location(
        module_name, module_file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    if 'modules' not in module.__dict__:
        sys.stderr.write(colored(
            f"Warning: file \"{module_file_path}\" doesn't contain \"modules\" dict. Using the defaults.\n", 'red'))
    else:
        try:
            module_result = module.modules
        except:
            module_result = default_modules

    

    return module_result


def is_file_readable(filename):
    if os.access(filename, os.R_OK):
        return True
    else:
        return False


def create_banner(address):
    result = "\n"
    line = "------- " + address + " -------"
    line_len = len(line)
    result += (colored("-" * line_len, "grey", attrs=["bold"])) + "\n"
    result += (colored(line[:7], "grey", attrs=["bold"]) +
               colored(line[7:-7], "red", attrs=["bold"]) +
               colored(line[-7:], "grey", attrs=["bold"])) + "\n"
    result += (colored("-" * line_len, "grey", attrs=["bold"]))
    return result


def get_switched_on(config, modules):
    """
    Finds which modules are "switched_on" and therefore will be run.

    Also check if each entry in config file has the corresponding module in module file. 
    If not, then the function either prints a warning (if it has switched_on=0) or exits with an error (if switched_on=1)

    """

    enabled_sections = []
    for section in config.sections():
        if section[-2:] == '_s':
            continue  # "nmap_s" and "masscan_s" will be ignored
        if not module_exists(section, modules):
            not_eixsting = True
        else:
            not_eixsting = False

        if not_eixsting:
            if config.getint(section, 'switched_on') == 1:
                exit_code = 128
                sys.exit("Error {}: module \"{}\" switched on but not defined (no record).".format(
                    exit_code, section))
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
            nmap_command, param = assist.craftNmapCommand(
                target, config, settings['NmapOutput']['output'])
            nmap_found_targets[target] = portFuncs.thePortScan(
                "nmap", nmap_command, param)

    if config['Masscan_s'].getboolean('switched_on'):
        doneAtLeastOneScan = True
        for target in targetS:
            masscan_command, param = assist.craftMasscanCommand(
                target, config, settings['MasscanOutput']['output'])

            try:
                masscan_found_target[target] = portFuncs.thePortScan(
                    "masscan", masscan_command, param)
            except:
                masscan_found_target[target] = classes.ip(target, None)

    if not doneAtLeastOneScan:

        exit_code = 89
        sys.exit(
            "Error {}: At least one scan must be performed:  nmap / masscan".format(exit_code))

    info = {}
    to_s_cim_pracujeme = {**masscan_found_target, **nmap_found_targets}
    for x in list(to_s_cim_pracujeme.keys()):
        info[x] = colored("Ports (" + x + ")\n", "grey", attrs=["bold"])
        # for port in to_s_cim_pracujeme[x].not_closed_not_filtered_ports():
        for port in to_s_cim_pracujeme[x].ports:
            info[x] += str(port) + "\n"

    return {**nmap_found_targets, **masscan_found_target}, info


def divideField(txt):
    path = txt.rsplit(".", 1)[0]
    func = txt.rsplit(".", 1)[1]
    return path, func


def service_check(module_service, real_services):
    if module_service == 'ANY' or module_service in real_services:
        return True
    else:
        return False


def performScanType1(targetS, overwrite, outputmanagment):

    targetS = [extract_domain_name(x) for x in targetS]
    config = configparser.RawConfigParser()
    settings = configparser.RawConfigParser()

    dir_path = os.path.dirname(os.path.abspath(__file__))

    type_one_file = get_type_one_file_because_possible_overwrite(
        overwrite, dir_path)
    
    modules = get_modules_because_possible_overwrite(
        overwrite, dipmodules.modules)
    settings_file = os.path.join(dir_path, "secondary", "conf", "settings.cfg")

    config.read(type_one_file)
    settings.read(settings_file)

    switched_ons = get_switched_on(config, modules)
    found_targets, info_output_about_ports = portScanningPhase(
        targetS, config, settings)

    for target in list(found_targets.keys()):

        print_according_to_outputmanagment(
            outputmanagment, create_banner(target))
        print_according_to_outputmanagment(
            outputmanagment, info_output_about_ports[target])

        if (found_targets[target] == None):
            print_according_to_outputmanagment(
                outputmanagment, colored("..probably down", 'red'))
            continue
        for switched_on_module in switched_ons:
            check_correct_form_of_module(switched_on_module, modules)
            print_according_to_outputmanagment(
                outputmanagment, "Module: " + colored(str(switched_on_module), "white", attrs=['bold']))
            ports = [
                p for p in found_targets[target].not_closed_not_filtered_ports()]
            for open_port in ports:
                if (modules[switched_on_module]['service'] == open_port.port_service):
                    path_of_command_cretor, command_creator_fun = divideField(
                        modules[switched_on_module]['command'])
                
                    correctModule_of_create_command_fun = safe_import(path_of_command_cretor)
                    cmd = getattr(
                        correctModule_of_create_command_fun,
                        command_creator_fun
                    )(
                        target,
                        open_port,
                        modules[switched_on_module]['params']
                    )

                    if 'additional' in modules[switched_on_module]:
                        path_of_additional, func_of_additional = divideField(
                            modules[switched_on_module]['additional'])
                        
                        correctModule_of_additional = safe_import(path_of_additional)

                        getattr(
                            correctModule_of_additional,
                            func_of_additional
                        )(
                            cmd,
                            target,
                            open_port,
                            modules[switched_on_module],
                            print_according_to_outputmanagment,
                            outputmanagment
                        )
                    if not modules[switched_on_module]['image'] == None and not '_abort_regular_run' in modules[switched_on_module]:
                        print_according_to_outputmanagment(
                            outputmanagment, launchTheScan(modules[switched_on_module], cmd))
                   

    return


def performScanType0(scan_after_discovery, overwrite, outputmanagment):

    config = configparser.RawConfigParser()
    settings = configparser.RawConfigParser()

    dir_path = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(dir_path, "secondary", "conf", "settings.cfg")
    # settings.read('src/secondary/conf/settings.cfg')
    settings.read(config_file)
    type_zero_file = os.path.join(dir_path, settings['Path']['typezeroConf'])
    config = configparser.RawConfigParser()
    config.read(type_zero_file)

    our_interfaces = getInterfaces(
        config['Interfaces'], config['Logic'].getboolean('negative'))
    interfaces = netifaces.interfaces()

    potentional_targets = []
    for inter in interfaces:
        if gonna_be_scanned(our_interfaces, inter, config['Logic'].getboolean('negative')):
            ip = netifaces.ifaddresses(inter)[netifaces.AF_INET][0]['addr']
            netmask = netifaces.ifaddresses(
                inter)[netifaces.AF_INET][0]['netmask']
            full_ip = str(ip) + "/" + str(netmaskToSlash(netmask))
            potentional_targets.append(str(full_ip))

    for target in potentional_targets:
        discovery_command, parameter = assist.craftHostDiscoveryNmapCommand(
            target, config, settings['NmapOutput']['output'])
        discovery_result = portFuncs.thePortScan(
            "Nmap_s", discovery_command, parameter)
        print_according_to_outputmanagment(
            outputmanagment, discovery_result[0])

    match scan_after_discovery:
        case '0':
            pass
        case '1':
            performScanType1(discovery_result[1], overwrite, outputmanagment)

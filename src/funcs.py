import docker # for docker images and containers managment
import configparser # for parsing the configuration file
from ftplib import FTP
import importlib

# from secondary.dockerimages import images
from src.secondary.dockerimages import tools

# import parsers.nmap.nmapparse as nmapparse
# import parsers.shcheck.shcheckparse as shcheckparse
# import parsers.cewl.cewlparse as cewlparse
# import parsers.masscan.masscanparse as masscanparse
# import parsers.dnsrecon.dnsreconparse as dnsreconparse
# import parsers.gobuster.gobusterparse as gobusterparse
# import parsers.nmap.nmapSSLparse as nmapSSLparse
# import parsers.nmap.nmapdiscoveryparse as nmapdiscoveryparse



""" Tried to solve the path problem but ending with this:
ABS: /usr/local/lib/python3.11/dist-packages/DIP-0.1.0-py3.11.egg/src/funcs.py/src.parsers.nmap.nmapparse
which is not good because the "dot" notation probably doesn't work very well with dots in some upper folders

So this commented code wasn't helpful at all


def launchTheScan (tool, command, param):
    dir_path = os.path.abspath(os.path.abspath(__file__))

    parser, img = getParserAndImage(tool, param)
    path_of_parser, func_in_parser = divideParserField(parser)
    absolute_parser_path = os.path.join(dir_path, path_of_parser)
    print("ABS: " + str(absolute_parser_path))
    correctModule = importlib.import_module(absolute_parser_path)
    dckr = docker.from_env()
    x = dckr.containers.run(img, command, detach = True )
    output = dckr.containers.get(x.id)
    
    return getattr(correctModule, func_in_parser)(output)

# "usr.local.lib.python3.11.dist-packages.DIP-0.1.0-py3.11.egg.src.parsers.nmap.nmapparse"

"""

def launchTheScan (tool, command, param):
    # print("Tool: " + tool)
    # print("Command: " + command)
    # print("Param?: " + param)
    parser, img = getParserAndImage(tool, param)
    # print("Parser: " + parser)
    # print("Img: " + img)
    path_of_parser, func_in_parser = divideParserField(parser)
    # print("Path of parser: " + path_of_parser)
    # print("Func in parser: " + func_in_parser)
    correctModule = importlib.import_module(path_of_parser)
    dckr = docker.from_env()
    x = dckr.containers.run(img, command, detach = True )
    output = dckr.containers.get(x.id)
    
    return getattr(correctModule, func_in_parser)(output)



# divide 'parser' field from the mapping function
# to the module path and to the fuction insied it
def divideParserField(txt):
    path = txt.rsplit(".",1)[0]
    func = txt.rsplit(".",1)[1]
    return path, func

def getParserAndImage(tool, param):
    for record in tools:
        if record['tool'] == tool and \
            (param in record['params'] or \
                'ANY' in record['params']):
            return record['parser'], record['image']



    exit("Error: correcponding module does not exist: " + str(tool) + " with the parameter '" + str(param) + "' "    "\
          \nIt seems like the specified combination of a tool and parameters is not covered in any module. Or maybe just a misspell?")




"""

def nmapOpenPortsDiscoverScan(target, nmap_command, debug_on):
    dckr = docker.from_env()
    x = dckr.containers.run(images["nmap"], " " + nmap_command + " " + target, detach = True)
    output = dckr.containers.get(x.id)
    
    return nmapparse.parse_output(
        target, output, debug_on
    )



def shcheckScan(target_ip, port):
    dckr = docker.from_env()
    print("I am SH-check!" + str(port))
    service = port.port_service
    if service == "http":
        shcheck_target = "http://" + str(target_ip.address)
    elif service == "https":
        shcheck_target = "https://" + str(target_ip.address )
    else:
        raise("Err # TODO")
    print(shcheck_target)
    print(images["shcheck"])
    x = dckr.containers.run(images["shcheck"], config['Shcheck']['params'] + " " + shcheck_target, detach = True) 
    output = dckr.containers.get(x.id)
    
    return shcheckparse.parse_output(
        output
    )

def shcheckScan2(command):
    dckr = docker.from_env()
    
    x = dckr.containers.run(
        images["shcheck"], 
        command,
        detach = True) 
    output = dckr.containers.get(x.id)

    return shcheckparse.parse_output(
        output
    )

def whatwebScan(target):
    dckr = docker.from_env()
    x = dckr.containers.run(images["whatweb"], config['Whatweb']['params'] + " " + target.address, detach = True )
    output = dckr.containers.get(x.id)
    
    return whatwebparse_basic.parse_output(
        output
    )

def whatwebScan2(whatweb_command, param):
    tool = "whatweb"
    return launchTheScan(tool,whatweb_command, param)

# Masscan potrebuje porty, v configuraku je zatial top 10
def masscanScan(target):
    dckr = docker.from_env()
    x = dckr.containers.run(images["masscan"], config['Masscan']['params'] + " " + target.address, detach = True )

    output = dckr.containers.get(x.id)

    return masscanparse.parse_output(
        output
    )

def dnsreconScan(target):
    dckr = docker.from_env()
    x = dckr.containers.run(images["dnsrecon"], config['Dnsrecon']['params'] + " " + target.address, detach = True )
   # with open(dnsjsonfile, 'r') as file:
     #   output = file.read()
    
    output = dckr.containers.get(x.id)
   

    return dnsreconparse.parse_output(
        output
    )



def nmapSSLScan(target_ip):
    dckr = docker.from_env()
    x = dckr.containers.run(images["nmap"],
                            config["Nmap"]["sslcert"] + " " +
                            target_ip.address,
                            detach=True
                            )
    output = dckr.containers.get(x.id)
    
    return nmapSSLparse.parse_output(
        output)



def gobusterScan(target_ip, port):

    dckr = docker.from_env()

    
    if port.port_service == "http":
        gobuster_target = "http://" + str(target_ip.address)
    elif port.port_service == "https":
        gobuster_target = "https://" + str(target_ip.address)
    x = dckr.containers.run(images["gobuster"], 
                            config['Gobuster']['params'] + 
                            " " + " -w " + config['Gobuster']['wordlist'] +
                            " " + " -u " + gobuster_target,
                            detach = True )
    


    output = dckr.containers.get(x.id)
   

    return gobusterparse.parse_output(
        output
    )



def checkForFtpAnon(target_ip):
    ftp = FTP(target_ip.address)
    resp = ftp.login()
    print(resp)
    exit()


"""
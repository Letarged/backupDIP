import docker # for docker images and containers managment
import configparser # for parsing the configuration file
from ftplib import FTP
import importlib
import sys
from src.secondary.dockerimages import tools




def launchTheScan (moduleinfo, command):
    image = moduleinfo['image']
    path_of_parser, func_in_parser = divideParserField(moduleinfo['parser'])
    correctModule = importlib.import_module(path_of_parser)
    dckr = docker.from_env()
    try:
        x = dckr.containers.run(image, command, detach = True )
        output = dckr.containers.get(x.id)

        return getattr(correctModule, func_in_parser)(output)
    except:
            return("Something went wrong when running image \"{}\".".format(moduleinfo['image']))

    
    



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
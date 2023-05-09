import docker # for docker images and containers managment
import configparser # for parsing the configuration file
from ftplib import FTP
import importlib
import sys
from src.secondary.dipmodules import scantools




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
    for record in scantools:
        if record['tool'] == tool and \
            (param in record['params'] or \
                'ANY' in record['params']):
            return record['parser'], record['image']



    exit("Error: correcponding module does not exist: " + str(tool) + " with the parameter '" + str(param) + "' "    "\
          \nIt seems like the specified combination of a tool and parameters is not covered in any module. Or maybe just a misspell?")




from operator import mod
import docker # for docker images and containers managment
import configparser # for parsing the configuration file
from ftplib import FTP
import importlib
import sys
# from .scanCoordination import safe_import
#from src.secondary.dipmodules import scantools


def safe_import(module_path):
    try:
        # print("Regular: " + module_path)
        return importlib.import_module(module_path)
    except:
        path = module_path.rsplit("/", 1)[0]
        module_itself = module_path.split("/")[-1]
        # print("THIS THEN: " + path + " :: " + module_itself)
        sys.path.append(path)
        return importlib.import_module(module_itself)



def launchTheScan (moduleinfo, command):
    image = moduleinfo['image']
    path_of_parser, func_in_parser = divideParserField(moduleinfo['parser'])
    # correctModule = importlib.import_module(path_of_parser)
    correctModule = safe_import(path_of_parser)
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


    exit("Error: correcponding module does not exist: " + str(tool) + " with the parameter '" + str(param) + "' "    "\
          \nIt seems like the specified combination of a tool and parameters is not covered in any module. Or maybe just a misspell?")




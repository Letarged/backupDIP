# ------------------------------
# File: ./src/portFuncs.py
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

import docker
import importlib
import sys
from src.secondary.dipmodules import modules


def thePortScan (tool, command, param):
    parser, img = getParserAndImage(tool, param)
    path_of_parser, func_in_parser = divideParserField(parser)
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
    record = modules[tool]
    return record['parser'], record['image']


    exit_code = 90
    sys.exit("Error {}: correcponding module does not exist: {} with the parameter '{}' "    "\
          \nIt seems like the specified combination of a tool and parameters is not covered in any module. Or maybe just a misspell?.".format(
                exit_code, tool, param))



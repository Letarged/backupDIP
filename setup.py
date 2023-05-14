#!/usr/bin/python3


from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import setuptools
import shutil
import appdirs
import json
import os
import sys

destination_cfg_file = ""
PACKAGE_NAME = "dipscan"

def copy_config():
    config_dir_in_this_system = appdirs.user_config_dir("dipconf")

    if not os.path.exists(appdirs.user_config_dir()):
        os.mkdir(appdirs.user_config_dir())
    if not os.path.exists(config_dir_in_this_system):
        os.mkdir(config_dir_in_this_system)

    destination_cfg_file = os.path.join(config_dir_in_this_system, "run.cfg")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir) # set the current working directory to the path of the script
    current_path = os.getcwd()
    file_path = "src/secondary/conf/types/typeone.cfg"
    source_cfg_file = os.path.join(current_path, file_path)
    shutil.copyfile(source_cfg_file, destination_cfg_file) 

    file_path = "src/secondary/dipmodules.py"
    destination_cfg_file = os.path.join(config_dir_in_this_system, "dipmodules.py")
    source_cfg_file = os.path.join(current_path, file_path)

    shutil.copyfile(source_cfg_file, destination_cfg_file) 

    
class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        try:
            docker_version = subprocess.check_output(['docker', '-v']).decode('utf-8')
            print(f"Docker already installed: {docker_version}")
        except:
            subprocess.call(['sudo', 'apt-get', 'update'])
            subprocess.call(['sudo', 'apt-get', 'install', '-y', 'docker.io'])
            
        # libraries = ['docker', 'termcolor', 'xmltodict']
        # for library in libraries:
        #     subprocess.call(['pip', 'install', library])

        subprocess.call(['docker', 'run', 'ubuntu']) # pulling the base image (ubuntu is the base image)
        subprocess.call(['docker', 'build', '-t', 'dnmap:v1', './imagesFromDocker/nmap'])
        subprocess.call(['docker', 'build', '-t', 'dcewl:v1', './imagesFromDocker/cewl'])
        subprocess.call(['docker', 'build', '-t', 'dshcheck:v1', './imagesFromDocker/shcheck'])
        subprocess.call(['docker', 'build', '-t', 'dwhatweb:v1', './imagesFromDocker/whatweb'])
        subprocess.call(['docker', 'build', '-t', 'dmasscan:v1', './imagesFromDocker/masscan'])
        subprocess.call(['docker', 'build', '-t', 'ddnsrecon:v1', './imagesFromDocker/dnsrecon'])
        subprocess.call(['docker', 'build', '-t', 'dgobuster:v1', './imagesFromDocker/gobuster'])
        subprocess.call(['docker', 'build', '-t', 'dsslscan:v1', './imagesFromDocker/sslscan'])


setup(
    name=PACKAGE_NAME,
    version='0.1.0',
    author='Michal Rajecký',
    author_email='xrajec01@fit.vutbr.cz',
    packages= find_packages(),
    package_data={
        '': ['*.cfg'],
    },
    install_requires=[
        'docker==2.0.0',
        'netifaces==0.11.0',
        'termcolor==2.3.0',
        'xmltodict==0.12.0',
             
        
        
    ],
    entry_points={
        'console_scripts': [
            'dipscan=src.p:main'
        ]
    },
    cmdclass={
        'install': CustomInstallCommand,
    }
)

copy_config()
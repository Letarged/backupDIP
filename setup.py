#!/usr/bin/python3


from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess


class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        try:
            docker_version = subprocess.check_output(['docker', '-v']).decode('utf-8')
            print(f"Docker already installed: {docker_version}")
        except:
            subprocess.call(['sudo', 'apt-get', 'update'])
            subprocess.call(['sudo', 'apt-get', 'install', '-y', 'docker.io'])

        subprocess.call(['docker', 'run', 'ubuntu']) # pulling the base image (ubuntu is the base image)
        subprocess.call(['docker', 'build', '-t', 'dnmap:v1', 'imagesFromDocker/nmap/DockerFile'])
        subprocess.call(['docker', 'build', '-t', 'dcewl:v1', 'imagesFromDocker/cewl/DockerFile'])
        subprocess.call(['docker', 'build', '-t', 'dshcheck:v1', 'imagesFromDocker/shcheck/DockerFile'])
        subprocess.call(['docker', 'build', '-t', 'dwhatweb:v1', 'imagesFromDocker/whatweb/DockerFile'])
        subprocess.call(['docker', 'build', '-t', 'dmasscan:v1', 'imagesFromDocker/masscan/DockerFile'])
        subprocess.call(['docker', 'build', '-t', 'ddnsrecon:v1', 'imagesFromDocker/dnsrecon/DockerFile'])
        subprocess.call(['docker', 'build', '-t', 'dgobuster:v1', 'imagesFromDocker/gobuster/DockerFile'])


setup(
    name='DIP',
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
            'tst=src.p:main'
        ]
    },
    cmdclass={
        'install': CustomInstallCommand,
    }
)

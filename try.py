#!/usr/bin/python3

import shutil
import appdirs
import json
import os
import sys

DEFAULT_CONFIG = {
    "param1": "value1",
    "param2": "value2",
    "param3": "value3"
}

config_dir_in_this_system = appdirs.user_config_dir("dipconf")

if not os.path.exists(config_dir_in_this_system):
    os.mkdir(config_dir_in_this_system)


destination_cfg_file = os.path.join(config_dir_in_this_system, "run.cfg")
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir) # set the current working directory to the path of the script
file_path = "src/secondary/conf/types/typeone.cfg"
current_path = os.getcwd()
source_cfg_file = os.path.join(current_path, file_path)

# print("SRC: " + source_cfg_file)
# print("DST: " + destination_cfg_file)

shutil.copyfile(source_cfg_file, destination_cfg_file)









# Expand the '~' character to the user's home directory
home_dir = os.path.expanduser('~')

# Create the directory in the home directory
dir_path = os.path.join(home_dir, 'dipconf')
os.mkdir(dir_path)
print(dir_path)

CONFIG_FILE_PATH = os.path.expanduser("~/dipconf/.my_framework_config.json")
INSTALL_DIR = os.path.dirname(os.path.realpath(__file__))

def save_config():
    with open(CONFIG_FILE_PATH, "w") as f:
        json.dump(DEFAULT_CONFIG, f)

    with open(os.path.join(INSTALL_DIR, "my_framework_config.json"), "w") as f:
        json.dump(DEFAULT_CONFIG, f)

def load_config():
    try:
        with open(CONFIG_FILE_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        pass

    try:
        with open(os.path.join(INSTALL_DIR, "my_framework_config.json"), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        pass

    return DEFAULT_CONFIG

config = load_config()
# Modify config as needed
save_config()

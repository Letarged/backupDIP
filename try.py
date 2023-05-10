#!/usr/bin/python3

import shutil
import appdirs
import json
import os
import sys
import importlib

path = "/home/kali/Music/mus"
correct_module = importlib.import_module(path)

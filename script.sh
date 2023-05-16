#!/bin/bash

find . -name '*.py' -exec sh -c 'echo """\
# ------------------------------
# File: {}
# Description: 
#
# Mster'\''s Thesis: Tool for Automated Penetration Testing of Web Servers
# Year: 2023
# Tool: dipscan v0.1.0
# Author: Michal Rajecký
# Email: xrajec01@stud.fit.vutbr.cz
#
# BRNO UNIVERSITY OF TECHNOLOGY
# FACULTY OF INFORMATION TECHNOLOGY
# ------------------------------
""" > {}.tmp && cat {} >> {}.tmp && mv {}.tmp {}' \;

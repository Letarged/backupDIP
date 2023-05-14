#!/usr/bin/env python3

import requests
from termcolor import colored

def get_robots_txt(target):
    url = target + "/robots.txt"
    response = requests.get(url)

    result = ''

    if response.status_code == 200:
        result += colored(f'{url}:\n', 'green')
        content = response.text.split('\n')
        for line in content:
            result += colored(f'\t{line}\n', 'blue')
    else:
        result += colored(f'{url}: ', 'yellow', attrs=['dark']) + colored("not found", 'red', attrs=['bold'])
    
    return result

print(get_robots_txt('https://192.168.0.206/bWAPP'))
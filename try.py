#!/usr/bin/python3
import ftplib
from termcolor import colored
def foo():
    ftp_target_ip = "192.168.0.206"
    port = 21

    ftp = ftplib.FTP()
    ftp.connect(ftp_target_ip, port)
   # ftp.login()
    print("Logged")
    response = (ftp.login('anonymous', ''))
    if "Anonymous access granted" in response:
        print("Should be a success?")

    try:
        ftp = ftplib.FTP()
        ftp.connect(ftp_target_ip, port)
        ftp.login()
        print("Logged")
        print(ftp.login('anonymous', ''))
        # Anonymous access granted
        # Check if anonymous login is allowed
        if ftp.login('anonymous', ''):
            print(colored(f'[+] {ftp_target_ip} allows anonymous FTP login', 'green', attrs=['bold']))
        else:
            print( colored(f'[-] {ftp_target_ip} does not allow anonymous FTP login', 'red', attrs=['bold']))
        
        # Close the FTP connection
        ftp.quit()

    except:
        print( "FTP not accessible.")

foo()
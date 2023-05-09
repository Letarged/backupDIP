import ftplib
from src.cores.helper import check_ip_or_url
import socket
from termcolor import colored

def dummy(x,y,z):
    return ""
    
def run(cmd, target,port, module, paramsprint_according_to_outputmanagment, outputmanagment):
    if check_ip_or_url(target) == "ip":
        ftp_target_ip = target
    elif check_ip_or_url(target) == "url":
        ftp_target_ip =  socket.gethostbyname(target)

    try:
        ftp = ftplib.FTP()
        ftp.connect(ftp_target_ip, port)
        ftp.login()
        
        # Check if anonymous login is allowed
        if ftp.login('anonymous', ''):
            paramsprint_according_to_outputmanagment(outputmanagment, colored(f'[+] {ftp_target_ip} allows anonymous FTP login', 'green', attrs=['bold']))
        else:
            paramsprint_according_to_outputmanagment(outputmanagment, colored(f'[-] {ftp_target_ip} does not allow anonymous FTP login', 'red', attrs=['bold']))
        
        # Close the FTP connection
        ftp.quit()

    except:
        paramsprint_according_to_outputmanagment(outputmanagment, "FTP not accessible.")

    """
    if check_ip_or_url(target) == "ip":
        ftp_target_ip = target
    elif check_ip_or_url(target) == "url":
        dns_target_ip =  socket.gethostbyname(target)

    ftp = ftplib.FTP(dns_target_ip)
    ftp.login("anonymous", "")
    if ftp.getwelcome().startswith("220"):
        print (colored("FTPAnonymous login"))
        print("Anonymous login successful!")
    else:
        print("Anonymous login failed.")
    ftp.quit()
    """
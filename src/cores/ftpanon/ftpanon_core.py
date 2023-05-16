import ftplib
from src.cores.helper import check_ip_or_url
import socket
from termcolor import colored

def dummy(x,y,z):
    return ""
    
def run(cmd, target,port, module, paramsprint_according_to_outputmanagment, outputmanagment):
    if check_ip_or_url(target) == "ip":
        ftp_target_ip = target
    else:
        ftp_target_ip =  socket.gethostbyname(target)
    
    
    try:
        ftp = ftplib.FTP()
        ftp.connect(ftp_target_ip, port.num)
       
        
        # Check if anonymous login is allowed
        if "Anonymous access granted" in ftp.login('anonymous', ''):
            paramsprint_according_to_outputmanagment(outputmanagment, colored(f'[+] {ftp_target_ip} allows anonymous FTP login', 'green', attrs=['bold']))
        else:
            paramsprint_according_to_outputmanagment(outputmanagment, colored(f'[-] {ftp_target_ip} does not allow anonymous FTP login', 'red', attrs=['bold']))
        
        ftp.quit()

    except:
        paramsprint_according_to_outputmanagment(outputmanagment, "FTP not accessible.")

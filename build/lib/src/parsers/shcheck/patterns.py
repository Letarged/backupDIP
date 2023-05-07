from termcolor import colored

headers = {
    'X-XSS-Protection' : 'Possibility of cross-site scripting (XSS) attacks.', 
    'Strict-Transport-Security' : 'Possibility of man-in-the-middle attacks and session hijacking ', 
    'Content-Security-Policy' : 'Possibility of injection attacks, cross-site scripting (XSS) attacks, clickjacking, and other code injection exploits. ', 
    'Referrer-Policy' : 'Possibility of sensitive data leakage through URLs. ', 
    'X-Frame-Options' : 'Possibility of clickjacking attacks. ', 
    'X-Content-Type-Options' : 'Possibility of MIME type sniffing attacks. ', 
    'Permissions-Policy' : 'Possibility of unintended actions being performed on behalf of a user without their knowledge or consent. ', 
    'Cross-Origin-Embedder-Policy' : 'Potential for a website to be embedded within another website without proper authorization. ', 
    'Cross-Origin-Resource-Policy' : 'Risk of cross-site resource leakage, where sensitive data is accessed by unauthorized parties. ', 
    'Cross-Origin-Opener-Policy' : 'Possibility of cross-origin attacks, where an attacker can exploit vulnerabilities in one website to compromise another website on the same origin. ', 
    'Feature-Policy' : 'Possibility of unauthorized access to device features and APIs ', 
}

def generate_output(list_of_missing, target):

    report = colored('### ', 'grey') + colored('SHCHECK', 'white') + colored(' ###\n', 'grey')
    report += colored(target, 'grey') + "\n"
    report += colored("There are " + str(len(list_of_missing)) + ' missing headers: \n', 'blue')
    for missing in list_of_missing:
        report += '\t'
        report += (colored(missing, 'red') + ": ")
        if missing in headers:
            report += (colored(headers[missing], 'green') + "\n")
        else:
            report += (colored("Information about the header are missing\n", 'grey'))
    return report
            


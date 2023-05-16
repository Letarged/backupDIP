# ------------------------------
# File: ./src/secondary/dipmodules.py
# Description: Mapping modules
#
# Mster's Thesis: Tool for Automated Penetration Testing of Web Servers
# Year: 2023
# Tool: dipscan v0.1.0
# Author: Michal Rajecký
# Email: xrajec01@stud.fit.vutbr.cz
#
# BRNO UNIVERSITY OF TECHNOLOGY
# FACULTY OF INFORMATION TECHNOLOGY
# ------------------------------



modules = {
    'masscan': {
        'image' : 'dmasscan:v1',
        'service' : '',
        'params' : '',
        'parser' : 'src.parsers.masscan.masscanparse.parse_output'
    },
    'nmap': {
        'image' : 'dnmap:v1',
        'service' : '',
        'params' : '-sS',
        'parser' : 'src.parsers.nmap.nmapparse.parse_output'
    },
     'Nmap_s': {
        'image' : 'dnmap:v1',
        'service' : '',
        'params' : '-sn',
        'parser' : 'src.parsers.nmap.nmapdiscoveryparse.parse_output'
    },
    'Shcheck_basic' : {
        'image' : 'dshcheck:v1',
        'service' : 'https',
        'params' : '-d', 
        'command' : 'src.cores.shcheck.shckech_core.craftShcheckCommand', 
        'parser' : 'src.parsers.shcheck.shcheckparse.parse_output',
    },
    'Whatweb' : {
        'image' : 'dwhatweb:v1',
        'service' : 'https',
        'params' : '-a1',
        'command' : 'src.cores.whatweb.whatweb_core.craftWhatwebCommand',
        'parser' : 'src.parsers.whatweb.whatwebparse.parse_output_basic'

    },
    'Whatweb_http' : {
        'image' : 'dwhatweb:v1',
        'service' : 'http',
        'params' : '-a1',
        'command' : 'src.cores.whatweb.whatweb_core.craftWhatwebCommand',
        'parser' : 'src.parsers.whatweb.whatwebparse.parse_output_basic'

    },
    'Dnsrecon' : {
        'image' : 'ddnsrecon:v1',
        'service' : 'domain',
        'params' : '-t std',
        'command' : 'src.cores.dnsrecon.dnsrecon_cl.craftDnsreconCommand',
        'parser' : 'src.parsers.dnsrecon.dnsreconparse.parse_output'
     } ,
    'Dnsrecon_reverse' : {
        'image' : 'ddnsrecon:v1',
        'service' : 'domain',
        'params' : '', # there is parameter '-r' which is hardcoded
        'command' : 'src.cores.dnsrecon.dnsrecon_rev.craftDnsReverseLookupCommand',
        'parser' : 'src.parsers.dnsrecon.dnsreverseparse.parse_output'
    },
    'Cewl' : {
        'image' : 'dcewl:v1',
        'service' : 'https',
        'params' : '', # no parameters
        'additional' : 'src.cores.cewl.cewl_core.run',
        'command' : 'src.cores.cewl.cewl_core.craftCewlCommand',
        'parser' : 'src.parsers.cewl.cewlparse.parse_output',
        'outputfolder' : '/home/dipscanoutput',
        '_abort_regular_run': ''
    },
    'Cewl_http' : {
        'image' : 'dcewl:v1',
        'service' : 'http',
        'params' : '', # no parameters
        'additional' : 'src.cores.cewl.cewl_core.run',
        'command' : 'src.cores.cewl.cewl_core.craftCewlCommand',
        'parser' : 'src.parsers.cewl.cewlparse.parse_output',
        'outputfolder' : '/home/kali/cewl_outs/http',
        '_abort_regular_run': ''
    },
    'NmapSSL' : {
        'image' : 'dnmap:v1',
        'service' : 'https',
        'params' : '--script ssl-cert',
        'command' : 'src.cores.nmap.nmapssl.craftNmapSSLCommand',
        'parser' : 'src.parsers.nmap.nmapSSLparse.parse_output'
    },
    'Sslscan' : {
        'image' : 'dsslscan:v1',
        'service' : 'https',
        'params' : '--xml=-',
        'command' : 'src.cores.sslscan.sslscan_core.craftSSLSCANCommand',
        'parser' : 'src.parsers.sslscan.sslscanparse.parse_output'
    },
    'Gobuster' : {
        'image' : 'dgobuster:v1',
        'service' : 'https',
        'params' : '-k -q -w micro.txt -fw',
        'command' : 'src.cores.gobuster.gobuster_core.craftGobusterCommand',
        'parser' : 'src.parsers.gobuster.gobusterparse.parse_output',
    },
    'ftpAnonLogin' :{
        'image' : None,
        'service' : 'ftp',
        'params' :'',
        'command' : 'src.cores.ftpanon.ftpanon_core.dummy',
        'additional' : 'src.cores.ftpanon.ftpanon_core.run',
        'parser' : '',
        '_abort_regular_run': ''

    }
}
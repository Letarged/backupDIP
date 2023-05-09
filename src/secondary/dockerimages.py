images = {
    'nmap' : 'dnmap:v1',
    'cewl' : 'dcewl:v1',
    'shcheck' : 'dshcheck:v1',
    'whatweb' : 'dwhatweb:v1',
    'masscan' : 'dmasscan:v1',
    'dnsrecon' : 'ddnsrecon:v1',
    'gobuster' : 'dgobuster:v1'
}

meta = {
    'typeoneconf': 'src/secondary/conf/types/typeone.cfg'
}
# ANY
tools = [
    {
        'tool' : 'cewl',
        'image' : 'dcewl:v1',
        'params' : [''], # no parameters
        'parser' : 'src.parsers.cewl.cewlparse.parse_output'
    },
    {
        'tool' : 'whatweb',
        'image' : 'dwhatweb:v1',
        'params' : ['-a1'],
        'parser' : 'src.parsers.whatweb.whatwebparse.parse_output_basic'
    },
    {
        'identifier' : 'Shcheck_basic',
        'tool' : 'shcheck',
        'image' : 'dshcheck:v1',
        'service' : 'https',
        'params' : '', # no parameters
        'core' : 'src.cores.shcheck.shckech_core.run', 
        'parser' : 'src.parsers.shcheck.shcheckparse.parse_output'
    },
    {
        'tool' : 'nmap',
        'image' : 'dnmap:v1',
        'params' : ['-sn'], # ICMP Echo Request scan
        'parser' : 'src.parsers.nmap.nmapdiscoveryparse.parse_output'
    },
    {
        
        'identifier' : 'Nmap_ports_basic',
        'tool' : 'nmap',
        'image' : 'dnmap:v1',
        'service' : 'ANY',
        'params' : '-sS',
        'core' : 'src.cores.nmap.nmap_core.run', 
        'parser' : 'src.parsers.nmap.nmapparse.parse_output'
    },
    {
        'tool' : 'nmap',
        'image' : 'dnmap:v1',
        'params' : ['--script ssl-cert'],
        'parser' : 'src.parsers.nmap.nmapSSLparse.parse_output'
    },
    {
        'tool' : 'dnsrecon',
        'image' : 'ddnsrecon:v1',
        'params' : ['-t std'],
        'parser' : 'src.parsers.dnsrecon.dnsreconparse.parse_output'
    },
 {
        'tool' : 'dnsrecon',
        'image' : 'ddnsrecon:v1',
        'params' : ['-r'],
        'parser' : 'src.parsers.dnsrecon.dnsreverseparse.parse_output'
    },
    {
        'tool' : 'gobuster',
        'image' : 'dgobuster:v1',
        'params' : ['-k -q'],
        'parser' : 'src.parsers.gobuster.gobusterparse.parse_output'
    },
    {
        'tool' : 'masscan',
        'image' : 'dmasscan:v1',
        'params' : [''],
        'parser' : 'src.parsers.masscan.masscanparse.parse_output'
    }
    
]

modules = {
    # 'Nmap' : {},
    # 'Nmap' : {
    #     'tool' : 'nmap',
    #     'image' : 'dnmap:v1',
    #     'service' : 'ANY',
    #     'params' : '-sS', # no parameters
    #     'core' : 'src.cores.nmap.nmap_core.run', 
    #     'parser' : 'src.parsers.nmap.nmapparse.parse_output'
    # },
    'Shcheck_basic' : {
        'image' : 'dshcheck:v1',
        'service' : 'https',
        'params' : '-d', # disable SSL chceck
        'core' : 'src.cores.shcheck.shckech_core.run', 
        'command' : 'src.cores.shcheck.shckech_core.craftShcheckCommand', 
        'parser' : 'src.parsers.shcheck.shcheckparse.parse_output'
    },
    'Whatweb' : {
        'image' : 'dwhatweb:v1',
        'service' : 'https',
        'params' : '-a1',
        'core' : 'src.cores.whatweb.whatweb_core.run',
        'command' : 'src.cores.whatweb.whatweb_core.craftWhatwebCommand',
        'parser' : 'src.parsers.whatweb.whatwebparse.parse_output_basic'

    },
    'Dnsrecon' : {
        'image' : 'ddnsrecon:v1',
        'service' : 'domain',
        'params' : '-t std',
        'core' : 'src.cores.dnsrecon.dnsrecon_cl.run',
        'command' : 'src.cores.dnsrecon.dnsrecon_cl.craftDnsreconCommand',
        'parser' : 'src.parsers.dnsrecon.dnsreconparse.parse_output'
     } ,
    'Dnsrecon_reverse' : {
        'image' : 'ddnsrecon:v1',
        'service' : 'domain',
        'params' : '', # there is parameter '-r' which is hardcoded
        'core' : 'src.cores.dnsrecon.dnsrecon_rev.run',
        'command' : 'src.cores.dnsrecon.dnsrecon_rev.craftDnsReverseLookupCommand',
        'parser' : 'src.parsers.dnsrecon.dnsreverseparse.parse_output'
    },
    'Cewl' : {
        'image' : 'dcewl:v1',
        'service' : 'https',
        'params' : '', # no parameters
        'core' : 'src.cores.cewl.cewl_core.run',
        'additional' : 'src.cores.cewl.cewl_core.run',
        '_abort_classic' : '',
        'command' : 'src.cores.cewl.cewl_core.craftCewlCommand',
        'parser' : 'src.parsers.cewl.cewlparse.parse_output',
        'outputfolder' : '/home/kali/cewl_outs'
    },
    'NmapSSL' : {
        'image' : 'dnmap:v1',
        'service' : 'https',
        'params' : '--script ssl-cert',
        'core' : 'src.cores.nmap.nmapssl.run',
        'command' : 'src.cores.nmap.nmapssl.craftNmapSSLCommand',
        'parser' : 'src.parsers.nmap.nmapSSLparse.parse_output'
    },
    'Sslscan' : {
        'image' : 'dsslscan:v1',
        'service' : 'https',
        'params' : '--xml=-',
        'core' : 'src.cores.sslscan.sslscan_core.run',
        'command' : 'src.cores.sslscan.sslscan_core.craftSSLSCANCommand',
        'parser' : 'src.parsers.sslscan.sslscanparse.parse_output'
    },
    'Gobuster' : {
        'image' : 'dgobuster:v1',
        'service' : 'https',
        'params' : '-k -q -w micro.txt -fw',
        'core' : 'src.cores.gobuster.gobuster_core.run',
        'command' : 'src.cores.gobuster.gobuster_core.craftGobusterCommand',
        'parser' : 'src.parsers.gobuster.gobusterparse.parse_output',
    },
    'ftpAnonLogin' :{
        'image' : 'NONE',
        'service' : 'https',
        'core' : 'src.cores.ftpanon.ftpanon_core.run',
        'params' :'',
        'command' : 'src.cores.ftpanon.ftpanon_core.dummy',
        'additional' : 'src.cores.ftpanon.ftpanon_core.run',
        '_abort_classic' : '',
    },
    'vag' :{}
}
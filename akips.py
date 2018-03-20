#!/usr/bin/env python

import os
import json
import requests

akips_server = os.environ['AKIPS_HOST']
password = os.environ['AKIPS_PASS']
inventory = {'_meta': {'hostvars': {}}}

groupurl = 'https://{akips_server}/api-db?password={password};cmds=list+device+group'
groupresponse = requests.get(groupurl.format(akips_server=akips_server,
                                        password=password),
                        proxies={'http': None, 'https': None},
                        verify=os.path.dirname(os.path.realpath(__file__)) + "/cacert.cer")
grouplines = groupresponse.text.split('\n')

for group in grouplines:
    if group == 'maintenance_mode' or group == 'CS-Servers' or group == '':
        continue

    url = 'https://{akips_server}/api-db?password={password};cmds=mget+*+*+ping4+PING.icmpState+value+/up/+any+group+{group}'

    response = requests.get(url.format(akips_server=akips_server,
                                       password=password,
                                       group=group),
                            proxies={'http': None, 'https': None},
                            verify=os.path.dirname(os.path.realpath(__file__)) + "/cacert.cer")
    lines = response.text.split('\n')
    inventory[group] = {'hosts': []}

    for line in lines:
        if line == '':
            continue
        host = line.split(' ')[0]
        ip = line.split(',')[-1]
        inventory[group]['hosts'].append(host)
        inventory['_meta']['hostvars'][host] = {'ansible_host': ip}

print json.dumps(inventory)

